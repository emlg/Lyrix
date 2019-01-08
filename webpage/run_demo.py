# MLP for Pima Indians Dataset Serialize to JSON and HDF5
import numpy as np
import os
import sys
import pickle
import codecs
import csv
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, Model, model_from_json
from keras.layers import Input, Embedding, LSTM, Dense, concatenate, BatchNormalization, Dropout
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from flask import Flask,render_template, request,json

app = Flask(__name__)
@app.route('/') #NEED GET
def signUp():
    return render_template('index.html')
score_ = 0

lyrics_base = ['where can we go what can we do\nwe re lost alone removed confused\nlet down and torn apart\nseek knowledge from the heart\nrework the illustrations we are a new creation\nsearching for the tower where the bells ring on the hour\nwhere the present and the future don t look sour\nwe re telling everyone we know so we can say that everybody knows\ncan t feed a hungry mouth when it s closed\nteach lies why try\ngive up give in\npretend turn heads\nkeep up sink in\nmisguided from the start\nseek wisdom from the heart\nyou can try your best to please us\nwe ll bite the hand that feeds us\njust when our time was running out and patience wearing thin\nwe start again where to begin\nthere s room for many more if you can fit into the mold\nbut don t come in go chase the wind',
'sitin  by the tv sittin  drinkin  my wine\nmy friends all say that i m wasting time\ni m gonna wait right here just to get the right meat\ni been waiting for hours i can wait all week\ni m not talkin   bout love\nnot talkin   bout war\nget what i need from the girl next door\nbeen watchin  cartoons on the tv screen\nwhat i m looking for is long and lean\na ticket to ride i want my feet in the air\ni m gonna tell my baby that i just don t care\ni m not talkin   bout love\nnot talkin   bout war\nget what i need from the girl next door\nyeah get what i need oh yeah oh\nbeen runnin  down the scene with my gasoline\ni m feeling nasty and mighty mean\nsaid outta my way cause i m runnin  hot\ni got to show my baby just what i got\ni m not talkin   bout love\nnot talkin   bout war\ntake what i need from the girl next door\ni m not talkin   bout love\nnot talkin   bout war\ntake what i need from the girl next door\ni m not talkin   bout love\nnot talkin   bout war\nget what i need from the girl next door\nyeah i get what i need from that mojo yeah\noh',
'born into this world the sum parts of a man\ncreated through experiments from scientific hands\nand though i live and breathe i cannot understand\nwith the mind of a child if this is what they planned\nlook upon me then hide away your face\ni am unlike you yet still i need a place\nwithin society where i can still be safe\nfrom all the ignorance of the human race\ni can try i still don t know why\nthey wanna lock me away\nfrom all i ve seen it makes no sense to me\nthey make a monster everyday\nthey make a monster everyday\nthey make a monster everyday\nthey make a monster everyday\nthey make a monster everyday',
'face against the ground\ntorn but you can stand\nyour will is strong but you have now\ni know you can save us\nfaith is on your side\nfears you can t deny\nit s burned a hole right through your soul\nbut i know you can save us\nsave us now\ndon t say goodbye\ni know you can save us\ndon t wave goodbye\nbut nothing can break us\ndon t say goodbye\ni know you can save us\nyou can bring us back again\nborn to be as one\nturn to face the sun\nyour will is strong but you have now\ni know you can save us\nsave us now\ndon t say goodbye\ni know you can save us\ndon t wave goodbye\nbut nothing can break us\ndon t say goodbye\ni know you can save us\nyou can bring us back again\nyou can bring us back again\nface against the ground\ntorn but you can stand\nyour will is strong but you have now\ni know you can save us\ndon t say goodbye\ni know you can save us\ndon t wave goodbye\nbut nothing can break us\ndon t say goodbye\ni know you can save us\nyou can bring us back again\ndon t say goodbye\ni know you can save us\ndon t wave goodbye\nbut nothing can break us\ndon t say goodbye\ni know you can save us\nyou can bring us back again\nyou can bring us back again',
'wait a minute my friend\ndon t pass me up for dead\nas babylon crumbles to sand\na sweet flower blossoms in my hand\nanother day is ending for you\nanother day\nwhile i m alive you see my rivers flowing\ndon t want to be like you\nthere are no wild beasts in here i know\nthere are no wild beasts in here we know\nand a voice of the people cries\nas it drones on in monotone\nhere is the news it s all so sad sad\nooh and those black and whites\nbut thy knew it\ntook a few and those panties in acquainted ways\ncome on\ncome on\ncome on away yeah\nwait a minute my friend\ndon t pass me up for dead\nas babylon crumbles to sand\na sweet flower blossoms in my hand\nanother day is ending for you\nanother day another day\ni m alive\nyou see my body burning\nburning up in here\nthere are no others in here i know\nthere are no others in here oh no\nburning up in here\nyou know you know\nstep a little closer\ni wonder if you can\nremember me in this way'
]

@app.route('/create', methods=['POST'])
def query_muse():
    def get_nearest_embed(emb, genre):
        if genre == 'pop':
            idx = neigh_pop.kneighbors([emb],return_distance=False)
            return muse_emb_pop[idx][0]
        elif genre == 'rock':
            idx = neigh_rock.kneighbors([emb],return_distance=False)
            return muse_emb_rock[idx][0]

    def get_swap_word(w, nb_neighbor, genre):
        emb = muse_voc2embed_rock[w]
        nearest_pop_emb = get_nearest_embed(emb, genre)
        words = []
        for i in range(3):
            words.append(muse_embed2voc_pop[tuple(list(nearest_pop_emb[i]))])
        return words[nb_neighbor], words


    #print("arrived in python")
    max_nb = int(request.form['max_nb'])
    src_genre = request.form['src_genre']
    trg_genre = request.form['trg_genre']
    input_lyrics = lyrics_base[int(request.form['song'])]
    rock_specific = pickle.load(open("rock_specific.p", "rb"))

    words_spec_rock = []
    for w in input_lyrics.split(' '):
        if w in rock_specific:
            words_spec_rock.append(w)

    tfidf_rock = pickle.load(open("tfidf_rock.p", "rb"))
    words_in_tfidf = []
    idx_of_tfidf = []
    for w in input_lyrics.split(' '):
        idx = np.where(tfidf_rock==w)[0]
        if len(idx)!= 0:
            words_in_tfidf.append(w)
            idx_of_tfidf.append(idx[0])
    ordered_terms = np.array(words_in_tfidf)[np.argsort(idx_of_tfidf)]
    SWAP_ROCK = list(set(words_spec_rock))
    muse_voc2embed_rock= pickle.load(open("voc2embed_rock.p", "rb"))
    muse_embed2voc_pop = pickle.load(open("embed2voc_pop.p", "rb"))
    muse_emb_pop = pickle.load(open("muse_emb_pop.p", "rb"))

    neigh_pop = pickle.load(open("neigh_pop.p", "rb"))

    swap = {}
    for w in SWAP_ROCK:
        new_word, neighbor_words = get_swap_word(w, 0, 'pop')
        print(w, '--> ', neighbor_words)
        swap[w] = new_word

    print('-----')
    i = 0
    while len(swap.keys()) < 10 and i < len(ordered_terms):
        w = ordered_terms[i]
        if w not in swap.keys():
            try:
                new_word, neighbor_words = get_swap_word(w, 1, 'pop')
                print(w, '--> ', neighbor_words)
                swap[w] = new_word
            except :
                print("error for ", w)
        i += 1

    return str(swap);

def get_words_to_change(lyrics, genre_typical_words, genre_word_pos_dict, amount = 10):
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
    lyrics_tokens = (n - 1) * [0] + [tokenizer.word_index[w] for w in lyrics] # Append 0 tokens at beginning in case of

    # Get the tokens ngrams for sentences before the tokens to change (input of the neural net)
    ngrams_with_output = np.array(ngram_lyrics(n, lyrics_tokens, samples_tokens = tokens_to_change))
    input_ngrams = ngrams_with_output[:,:-1]
    output = ngrams_with_output[:,-1]

    # Get the POS of tokens that we want to predict
    tok_pos_dict = {tokenizer.word_index[w] : genre_word_pos_dict[w] for w in words_to_change}
    _, input_onehot_pos = token_to_onehot(output, pos_index_dict, tok_pos_dict)

    # Get the #syllables of tokens that we want to predict
    tok_syllab_dict = {tokenizer.word_index[w]:len(syllables_dic.inserted(w).split('-')) for w in words_to_change}
    _, input_onehot_syl = token_to_onehot(output, syl_index_dict, tok_syllab_dict)

    nn_input = [input_ngrams, input_onehot_pos, input_onehot_syl]
    return nn_input, output


def predict_new_words(g2_nn_model, g1_nn_input, outputs_tokens, g2_outnn_token_dict):
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
    # real_pred_list sorted in order of apparition
    new_lyrics = []
    idx = 0
    for w in lyrics:
        if idx < len(real_pred_list):
            real_w, pred_w = real_pred_list[idx]
        if w == real_w:
            new_lyrics.append('<b>' + pred_w + '</b>')
            idx += 1
        else:
            new_lyrics.append(w)
    print("Converted lyrics:")
    printmd(' '.join(new_lyrics) + '\n')
    return new_lyrics

def csv_to_dict(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        dict_ = dict(reader)
    return dict_

def load_all_data_for_genre(genre, tokenizer):
    """Helper function that loads all the useful data (neural net model, training history,
    outnn_token_dict for samples trained on this genre...) for a given genre (path where the data are given)"""
    path_nn = 'data/NN_models/' + genre + '/' + genre + '_best_200k'
    # Load neural net model and history
    nn_model, training_hist = load_model(path_nn, True)
    #print("Genre {} , max validation accuracy: {}".format(genre, max(training_hist['val_categorical_accuracy'])))
    # Load dictionary of {tokens -> output in neural net}
    token_outnn_dict = load_dict(path_nn + '/token_outnn_dict')
    outnn_token_dict = dict(zip(token_outnn_dict.values(), token_outnn_dict.keys()))
    return nn_model, token_outnn_dict

@app.route('/predict', methods=['POST'])
def query_nn():
    #Retrieve the parameters
    max_nb = int(request.form['max_nb'])
    src_genre = request.form['src_genre']
    trg_genre = request.form['trg_genre']
    input_lyrics = lyrics_base[int(request.form['song'])]

    # Load tokenizer
    tokenizer = pickle.load(open('../data/NN_models/tokenizer', 'rb'))
    src_word_pos_dict = csv_to_dict('../data/NN_models/' + src_genre + '/' + src_genre + '_word_pos.csv')
    pos_to_keep = {'INTJ','NOUN','ADV','PRON','VERB','ADP','DET','CCONJ','ADJ','NUM','PROPN'}
    src_word_pos_dict = {k:v for k,v in src_word_pos_dict.items() if v in pos_to_keep}

    src_diff_list = pickle.load(open("../data/NN_models/"+src_genre+"/"+src_genre+"_diff_list.p", "rb"))

    src_nn_input, src_output = get_words_to_change(input_lyrics, src_diff_list, src_word_pos_dict, max_nb)
    trg_nn_model,trg_outnn_token_dict = load_all_data_for_genre(trg_genre, tokenizer)
    trg_preds_list = predict_new_words(trg_nn_model, src_nn_input, src_output, trg_outnn_token_dict)
    trg_src_lyrs = get_new_lyrics(src_song, trg_preds_list)
    return trg_src_lyrs

if __name__ == "__main__":
    app.run()
