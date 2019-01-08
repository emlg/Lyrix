import numpy as np
import os
import sys
import pickle
import codecs
import csv
import pyphen
from keras.models import model_from_json
from keras.utils import to_categorical

def load_dict(path):
    with open(path, 'rb') as handle:
        dict_ = pickle.load(handle)
    return dict_

def ngram_lyrics(n, lyrs, samples_tokens = None):
    """
    Compute ngrams for one given lyrics (padded), if samples tokens different of None, keep only the ngrams ending 
    with tokens in samples_tokens
    """
    
    # Add first ngrams with some zeros
    ngram_lyrs = []
    for i in range(n):
        end_index = i + 2 
        first_elems = lyrs[: end_index]
        last_elem = first_elems[-1]
        # Append to ngrams if last elem (element to predict) is in samples
        if len(first_elems) < n and last_elem in samples_tokens:
            ngram = (n - end_index)*[0]
            for elem in first_elems:
                ngram.append(elem)
            ngram_lyrs.append(ngram)
    
    # Add rest of ngrams with no zeros
    for i, _ in enumerate(lyrs[: -n + 1]):
        n_gram = lyrs[i : i + n] # take the element and next n - 1 ones
        last_elem = n_gram[-1]
        # Append to ngrams if last elem (element to predict) is in samples
        if last_elem in samples_tokens:
            ngram_lyrs.append(n_gram)
    
    return ngram_lyrs

def token_to_onehot(Y, token_idx_dict, token_pos_dict = None):
    if token_pos_dict != None:
        # POS of y one hot encoding
        pos_y = [token_pos_dict[y] for y in Y]
        new_Y = [token_idx_dict[pos] for pos in pos_y]
    else:
        # Vocabulary of y one hot encoding
        new_Y = [token_idx_dict[y] for y in Y]
    # For 1 hot encod:
    one_hot_Y = to_categorical(new_Y, num_classes = len(token_idx_dict))
    return new_Y, one_hot_Y

def onehot_to_token(one_hot_Y, idx_token_dict):
    idx_y = np.argmax(one_hot_Y, axis = 1) # Get argmax of each row
    Y = [idx_token_dict[i] for i in idx_y]
    return Y

def get_words_to_change(lyrics, tokenizer, genre_typical_words, genre_word_pos_dict, amount = 10):
    """
    Function that gets the most common words in the lyrics given a sorted list for a specific genre
    lyrics: list of strings (the lyrics of a song)
    genre_typical_words: the sorted list of typical words of a genre (pop_diff_list for pop), format: tuples (word, diff_count)
    amount: the number of words we want to change in the lyrics
    """
    words_to_change = []
    words_to_change_pos = []
    found_words = 0
    for w, _ in genre_typical_words:
        if w in lyrics:
            words_to_change.append(w)
            words_to_change_pos.append([(word, i) for i, word in enumerate(lyrics) if word == w])
            found_words += 1
        if found_words == amount:
            break
    print("List of words to change in the lyrics: {}".format(words_to_change))
    words_to_change_pos = [w for l in words_to_change_pos for w in l]
    words_to_change_pos = sorted(words_to_change_pos, key = lambda x: x[1])

    tokens_to_change = [tokenizer.word_index[w] for w in words_to_change]
    ngram = 6
    lyrics_tokens = (ngram - 1) * [0] + [tokenizer.word_index[w] for w in lyrics if w in tokenizer.word_index.keys()] # Append 0 tokens at beginning in case of

    # Get the tokens ngrams for sentences before the tokens to change (input of the neural net)
    ngrams_with_output = np.array(ngram_lyrics(ngram, lyrics_tokens, samples_tokens = tokens_to_change))
    input_ngrams = ngrams_with_output[:,:-1]
    output = ngrams_with_output[:,-1]

    # Get the POS of tokens that we want to predict
    tok_pos_dict = {tokenizer.word_index[w] : genre_word_pos_dict[w] for w in words_to_change}
    pos_index_dict = load_dict('../data/NN_models/POS_index_dict')
    _, input_onehot_pos = token_to_onehot(output, pos_index_dict, tok_pos_dict)

    # Get the #syllables of tokens that we want to predict
    syllables_dic = pyphen.Pyphen(lang = 'en')
    tok_syllab_dict = {tokenizer.word_index[w]:len(syllables_dic.inserted(w).split('-')) for w in words_to_change}
    # This is the syllables -> index dictionary used for any genre in the NN training
    syl_index_dict = {1:0, 2:1, 3:2, 4:2}
    _, input_onehot_syl = token_to_onehot(output, syl_index_dict, tok_syllab_dict)

    nn_input = [input_ngrams, input_onehot_pos, input_onehot_syl]
    return nn_input, output


def predict_new_words(g2_nn_model, g1_nn_input, outputs_tokens, g2_outnn_token_dict, tokenizer):
    """
    Given neural network of other genre (g2) and input of genre 1 (g1) from the song,
    compute the prediction from g1 to g2
    """
    predictions_onehot = g2_nn_model.predict(g1_nn_input)
    pred_tokens = onehot_to_token(predictions_onehot, g2_outnn_token_dict)

    pred_words = [tokenizer.index_word[tok] for tok in pred_tokens]
    real_words = [tokenizer.index_word[tok] for tok in outputs_tokens]

    return list(zip(real_words, pred_words))

def get_new_lyrics(lyrics, real_pred_list):
    """
    Function that gives the new lyrics based on predictions generated from the other genre
    real_pred_list: sorted list of apparition of tuples: (real word, predicted word)
    """
    lyrics_with_jump = lyrics.replace('\n', ' <br> ').split(' ')
    # real_pred_list sorted in order of apparition
    new_lyrics = []
    idx = 0
    for w in lyrics_with_jump:
        if idx < len(real_pred_list):
            real_w, pred_w = real_pred_list[idx]
        if w == real_w:
            new_lyrics.append('<b>' + pred_w + '</b>')
            idx += 1
        else:
            new_lyrics.append(w)
    return ' '.join(new_lyrics)

def csv_to_dict(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        dict_ = dict(reader)
    return dict_

def load_model(path, get_history):
    # load json and create model
    json_file = open(path + '/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    nn_model = model_from_json(loaded_model_json)
    # load weigths in the model 
    nn_model.load_weights(path + '/weights.h5')
    history = {}
    if get_history:
        with open(path + '/trainHistoryDict', 'rb') as file:
            history = pickle.load(file)
    return nn_model, history

def load_all_data_for_genre(genre, tokenizer):
    """Helper function that loads all the useful data (neural net model, training history,
    outnn_token_dict for samples trained on this genre...) for a given genre (path where the data are given)"""
    path_nn = '../data/NN_models/' + genre + '/' + genre + '_best_200k'
    # Load neural net model (not history)
    nn_model, _ = load_model(path_nn, False)
    #print("Genre {} , max validation accuracy: {}".format(genre, max(training_hist['val_categorical_accuracy'])))
    # Load dictionary of {tokens -> output in neural net}
    token_outnn_dict = load_dict(path_nn + '/token_outnn_dict')
    outnn_token_dict = dict(zip(token_outnn_dict.values(), token_outnn_dict.keys()))
    return nn_model, outnn_token_dict