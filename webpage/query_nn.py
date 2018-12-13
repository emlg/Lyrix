# MLP for Pima Indians Dataset Serialize to JSON and HDF5
import numpy as np
import os
import sys
import pickle
import codecs
from sklearn.neighbors import NearestNeighbors
from flask import Flask,render_template, request,json

app = Flask(__name__)
@app.route('/') #NEED GET
def signUp():
    return render_template('index.html')
score_ = 0

# Load embeddings
def load_embeddings(file_name):
    with codecs.open(file_name, 'r', 'utf-8') as f_in:
        lines = f_in.readlines()
        lines = lines[1:]
        vocabulary, wv = zip(*[line.strip().split(' ', 1) for line in lines])
    wv = np.loadtxt(wv)
    return wv, vocabulary

def get_dict(embed, voc):
    voc_embeds_dict = {}
    embeds_voc_dict = {}
    for v, emb in zip(voc, embed):
        voc_embeds_dict[v] = tuple(emb)
        embeds_voc_dict[tuple(emb)] = v
    return voc_embeds_dict, embeds_voc_dict


@app.route('/create', methods=['POST'])
def query():
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
    input_lyrics = request.form['l']
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
    SWAP_TFIDF = []
    i = 0
    while len(SWAP_ROCK) + len(SWAP_TFIDF) < max_nb:
        if ordered_terms[i] not in SWAP_ROCK and ordered_terms[i] not in SWAP_TFIDF:
            SWAP_TFIDF.append(ordered_terms[i])
        i += 1
    src_file = "vectors-cbow_" + src_genre + ".txt"
    trg_file = "vectors-cbow_" + trg_genre + ".txt"
    muse_emb_rock, muse_voc_rock = load_embeddings(src_file)
    muse_emb_pop, muse_voc_pop = load_embeddings(trg_file)
    muse_voc2embed_rock, muse_embed2voc_rock = get_dict(muse_emb_rock, muse_voc_rock)
    muse_voc2embed_pop, muse_embed2voc_pop = get_dict(muse_emb_pop, muse_voc_pop)

    neigh_pop = NearestNeighbors(n_neighbors=3)
    neigh_pop.fit(muse_emb_pop)
    neigh_rock = NearestNeighbors(n_neighbors=3)
    neigh_rock.fit(muse_emb_rock)

    swap = {}
    for w in SWAP_ROCK:
        new_word, neighbor_words = get_swap_word(w, 0, 'pop')
        #print(w, '--> ', neighbor_words)
        swap[w] = new_word

    #print('-----')
    for w in SWAP_TFIDF:
        new_word, neighbor_words = get_swap_word(w, 1, 'pop')
        #print(w, '--> ', neighbor_words)
        swap[w] = new_word

    return str(swap);

if __name__ == "__main__":
    app.run()
