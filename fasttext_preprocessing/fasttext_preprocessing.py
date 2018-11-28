import sys
import codecs
import numpy as np

file_vec = 'model_lyrics3.vec'
file_bin = 'model_lyrics3.bin'

def load_embeddings(file_name):
	"""
	Load the embeddings from the .vec file given as input
	"""
	with codecs.open(file_name, 'r', 'utf-8') as f_in:
		lines = f_in.readlines()
		lines = lines[1:]
		vocabulary, wv = zip(*[line.strip().split(' ', 1) for line in lines])
		wv = np.loadtxt(wv)
	return wv, vocabulary
