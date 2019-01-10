# MLP for Pima Indians Dataset Serialize to JSON and HDF5
import numpy as np
import os
import sys
import pickle
import codecs
import csv
import pyphen
from nn_helpers import *
from keras.models import model_from_json
from keras.utils import to_categorical
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
'wait a minute my friend\ndon t pass me up for dead\nas babylon crumbles to sand\na sweet flower blossoms in my hand\nanother day is ending for you\nanother day\nwhile i m alive you see my rivers flowing\ndon t want to be like you\nthere are no wild beasts in here i know\nthere are no wild beasts in here we know\nand a voice of the people cries\nas it drones on in monotone\nhere is the news it s all so sad sad\nooh and those black and whites\nbut thy knew it\ntook a few and those panties in acquainted ways\ncome on\ncome on\ncome on away yeah\nwait a minute my friend\ndon t pass me up for dead\nas babylon crumbles to sand\na sweet flower blossoms in my hand\nanother day is ending for you\nanother day another day\ni m alive\nyou see my body burning\nburning up in here\nthere are no others in here i know\nthere are no others in here oh no\nburning up in here\nyou know you know\nstep a little closer\ni wonder if you can\nremember me in this way',
'all the single ladies \nall the single ladies \nall the single ladies \nall the single ladies now put your hands up\nup in the club  we just broke up  i m doing my own little thing\ndecided to dip and now you wanna trip \n cause another brother noticed me\ni m up on him he up on me\ndon t pay him any attention\njust cried my tears for three good years\nyou can t get mad at me\n cause if you liked it then you should have put a ring on it\nif you liked it then you shoulda put a ring on it\ndon t be mad once you see that he want it\n cause if you liked it then you shoulda put a ring on it\noh oh oh oh oh oh oh oh oh oh oh oh \nif you liked it then you should have put a ring on it\nif you liked it then you t be mad once you see that he want it\ndon t be mad once you see that he want it\nif you liked it then you shoulda put a ring on it\ni got gloss on my lips a man on my hips\ngot me tighter in my carryon jeans\nacting up drink in my cup\ni can t care less what you think\ni need no permission did i mention\ndon t pay him any attention\n cause you had your turn and now you gonna learn\nwhat it really feels like to miss me\n cause if you liked it then you should have put a ring on it\nif you liked it then you shoulda put a ring on it\ndon t be mad once you see that he want it\n cause if you liked it then you shoulda put a ring on it\noh oh oh oh oh oh\ndon t treat me to these things of the world\ni m not that kind of girl\nyour love is what i prefer what i deserve\nis a man that makes me then takes me\nand delivers me to a destiny to infinity and beyond\npull me into your arms\nsay i m the one you want\nif you don t you ll be alone\nand like a ghost i ll be gone\nall the single ladies\nall the single ladies \nall the single ladies \nall the single ladies now put your hands up\noh oh oh oh oh oh\n cause if you liked it then you should have put a ring on it\nif you liked it then you shoulda put a ring on it\ndon t be mad once you see that he want it\nif you liked it then you shoulda put a ring on it\noh oh oh\nif you liked it then you should have put a ring on it\nif you liked it then you shoulda put a ring on it\ndon t be mad once you see that he want it\nif you liked it then you shoulda put a ring on it oh oh oh',
'did you see that man in the limousine\nwith the pretty doll he is fifty and the girl s only seventeen\nbut she doesn t care and she never will\nif he s ninetyfive she don t give a damn\njust as long as he pays the bill\ndid you see that man with a fat cigar\nhe just left his lunch with a belly full of lobster and caviar\nhe can choose the wine from a vintage year\nhe will drink champagne in his limousine\nwhere the rest of the street can peer\n cause he s the man in the middle never second fiddle\njust like a spider in a cobweb\nhard as a hammer not the kind of boss you doublecross\n cause he s the man in the middle knows the way to diddle\nhe s never bothered by his conscience\ndeals with the devil  cause he wants to be\nman in the middle the middle the middle\nin the middle \nbut you see that man made a big mistake\neven though he s got all his servants and a mansion beside a lake\nand the money too all that he can spend\nhe can buy the most nearly anything\nbut he can t buy the lot his friend',
'it s close to midnight \nand something evil s lurking in the dark\nunder the moonlight \nyou see a sight that almost stops your heart\n\nyou try to scream\nbut terror takes the sound before you make it\nyou start to freeze \nas horror looks you right between the eyes\nyou re paralyzed\n\n cause this is thriller thriller night\nand no one s gonna save you from the beast about to strike\nyou know it s thriller thriller night\nyou re fighting for your life inside a killer thriller tonight yeah\n\noh oh oh\n\nyou hear the door slam \nand realize there s nowhere left to run\nyou feel the cold hand \nand wonder if you ll ever see the sun\n\nyou close your eyes \nand hope that this is just imagination\ngirl but all the while \nyou hear the creature creepin  up behind\nyou re out of time\n\n cause this is thriller thriller night\nthere ain t no second chance against the thing with forty eyes girl\nthriller thriller night\nyou re fighting for your life inside a killer thriller tonight\n\nnight creatures call\nand the dead start to walk in their masquerade\nthere s no escapin  the jaws of the alien this time \nthis is the end of your life oh\n\nthey re out to get you \nthere s demons closing in on every side\nthey will possess you \nunless you change that number on your dial\n\nnow is the time \nfor you and i to cuddle close together yeah\nall through the night \ni ll save you from the terrors on the screen\ni ll make you see\n\nthat it s a thriller thriller night\n cause i can thrill you more than any ghost would ever dare try\nthriller thriller night\nso let me hold you tight and share a killer diller \nchiller thriller here tonight\n\n cause it s a thriller thriller night\ngirl i can thrill you more than any ghost would ever dare try\nthriller thriller night\nso let me hold you tight and share a killer diller\n\ni m gonna thrill you tonight\ndarkness falls across the land\nthe midnight hour is close at hand\ncreatures crawl in search of blood\nto terrorize y awl s neighborhood\nand whosoever shall be found\nwithout the soul for getting down\nmust stand and face the hounds of hell\nand rot inside a corpse s shell\n\ni m gonna thrill you tonight\nthriller ohh baby \ni m gonna thrill you tonight \nthriller all night oh baby\ni m gonna thrill you tonight\nthriller thriller night \ni m gonna thrill you tonight\nthriller all night \nthriller night \n\nthe foulest stench is in the air\nthe funk of forty thousand years\nand grizzly ghouls from every tomb\nare closing in to seal your doom\nand though you fight to stay alive\nyour body starts to shiver\nfor no mere mortal can resist\nthe evil of the thriller',
'yesterday all my troubles seemed so far away\nnow it looks as though they re here to stay\noh i believe in yesterday\n\nsuddenly i m not half the man i used to be\nthere s a shadow hanging over me\noh yesterday came suddenly\n\nwhy she had to go i don t know she wouldn t say\ni said something wrong now i long for yesterday\n\nyesterday love was such an easy game to play\nnow i need a place to hide away\noh i believe in yesterday\n\nwhy she had to go i don t know she wouldn t say\ni said something wrong now i long for yesterday\n\nyesterday love was such an easy game to play\nnow i need a place to hide away\noh i believe in yesterday\nmm mm mm mm mm mm mm',
'now i ve been looking for someone\ntrying to find the right boy to wear on my arm\ni must admit it\nyou simply fit it\nyou were like a cut from the rest\nthat s why you re winning \nevery night when\ni close my eyes i can see you\nmy perfect type\nand i never really thought my dreams would come true\nuntil i laid eyes on you\n cause you know you are\nboyfriend material\nboyfriend material\nthat s what you re made of\nit s written on your label\nboyfriend material ma ma material\nwant everyone to know your my\nboyfriend material\nboyfriend material \nboyfriend material\nma ma material\nwant everyone to know that\nyou and your perfect smile\nare both timeless and never going out of style\nthere s so many reasons you got it together\nwhen i m catching feelings\nyou make me look better \nevery night when\ni close my eyes i can see you\nmy perfect type\nand i never really thought my dreams would come true\nuntil i laid eyes on you\n cause you know you are\nboyfriend material\nboyfriend material\nthat s what you re made of\nit s written on your label\nboyfriend material ma ma material\nwant everyone to know your my\nboyfriend material\nboyfriend material \nboyfriend material\nma ma material\nwant everyone to know\noh there ain t any other\nit s all the little things\nthat you do make me wanna sing yeah yeah\nthere ain t any other\nthe way you re talking to me i can tell you ve been listening\nto everything\nand maybe it s the butterflies\ni get every time i hear your ringtone \nand maybe it s  cause every single text boy\ni told myself you were the one yeah yeah\nboyfriend material\n cause i know you re boyfriend material\nboyfriend material\nthat s what you re made of\nit s written on your label\nboyfriend material ma ma material\nwant everyone to know your my\nboyfriend material  boyfriend material\nthat s what you re made of it s written on your label\nboyfriend material ma ma material\nwant everyone to know you re my\nboyfriend material\nboyfriend material\nboyfriend material\nma ma material\nwant everyone to know that'
]

@app.route('/create', methods=['POST'])
def query_muse():
    #print("arrived in python")
    max_nb = int(request.form['max_nb'])
    src = request.form['src_genre']
    trg = request.form['trg_genre']
    input_lyrics = lyrics_base[int(request.form['song'])]
    src_specific = pickle.load(open(src+"/specific_from_"+trg+".py", "rb"))
    muse_voc2embed_src= pickle.load(open(src+"/muse_voc2embed_with_"+trg+".py", "rb"))
    muse_embed2voc_trg = pickle.load(open(trg+"/muse_embed2voc_with_"+src+".py", "rb"))
    muse_emb_trg = pickle.load(open(trg+"/muse_emb_with_"+src+".py", "rb"))
    neigh_trg = NearestNeighbors(n_neighbors=3)
    neigh_trg.fit(muse_emb_trg)

    def get_nearest_embed(emb):
        idx = neigh_trg.kneighbors([emb],return_distance=False)
        return muse_emb_trg[idx][0]

    def get_swap_word(w, nb_neighbor):
        emb = muse_voc2embed_src[w]
        nearest_trg_emb = get_nearest_embed(emb)
        words = []
        for i in range(3):
            words.append(muse_embed2voc_trg[tuple(list(nearest_trg_emb[i]))])
        return words[nb_neighbor], words


    words_spec_src = []
    for w in input_lyrics.split(' '):
        if w in src_specific:
            words_spec_src.append(w)

    tfidf_src = pickle.load(open(src+"/tfidf.py", "rb"))
    words_in_tfidf = []
    idx_of_tfidf = []
    for w in input_lyrics.split(' '):
        idx = np.where(tfidf_src==w)[0]
        if len(idx)!= 0:
            words_in_tfidf.append(w)
            idx_of_tfidf.append(idx[0])
    ordered_terms = np.array(words_in_tfidf)[np.argsort(idx_of_tfidf)]
    SWAP_SRC = list(set(words_spec_src))

    swap = {}
    for w in SWAP_SRC:
        new_word, neighbor_words = get_swap_word(w, 0)
        print(w, '--> ', neighbor_words)
        swap[w] = new_word

    print('-----')
    i = 0
    while len(swap.keys()) < 10 and i < len(ordered_terms):
        w = ordered_terms[i]
        if w not in swap.keys():
            try:
                new_word, neighbor_words = get_swap_word(w, 1)
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
    lyrics_list_words = input_lyrics.replace('\n', ' ').split(' ')

    # Load tokenizer
    tokenizer = pickle.load(open('../data/NN_models/tokenizer', 'rb'))
    src_word_pos_dict = csv_to_dict('../data/NN_models/' + src_genre + '/' + src_genre + '_word_pos.csv')
    pos_to_keep = {'INTJ','NOUN','ADV','PRON','VERB','ADP','DET','CCONJ','ADJ','NUM','PROPN'}
    src_word_pos_dict = {k:v for k,v in src_word_pos_dict.items() if v in pos_to_keep}

    src_diff_list = pickle.load(open("../data/NN_models/"+src_genre+"/"+src_genre+"_diff_list.p", "rb"))

    src_nn_input, src_output = get_words_to_change(lyrics_list_words, tokenizer, src_diff_list, src_word_pos_dict, max_nb)
    trg_nn_model,trg_outnn_token_dict = load_all_data_for_genre(trg_genre, tokenizer)
    trg_preds_list = predict_new_words(trg_nn_model, src_nn_input, src_output, trg_outnn_token_dict, tokenizer)
    trg_src_lyrs = get_new_lyrics(input_lyrics, trg_preds_list)
    return trg_src_lyrs

if __name__ == "__main__":
    app.run()
