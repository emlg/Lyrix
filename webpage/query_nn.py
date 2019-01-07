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


@app.route('/predict', methods=['POST'])
def query_nn():
    #Retrieve the parameters
    max_nb = int(request.form['max_nb'])
    src_genre = request.form['src_genre']
    trg_genre = request.form['trg_genre']
    input_lyrics = lyrics_base[int(request.form['song'])]




if __name__ == "__main__":
    app.run()
