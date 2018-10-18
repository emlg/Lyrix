# MLP for Pima Indians Dataset Serialize to JSON and HDF5
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy
import os
import sys
from flask import Flask,render_template, request,json

app = Flask(__name__)
@app.route('/') #NEED GET
def signUp():
    return render_template('index.html')
score_ = 0

@app.route('/predict', methods=['POST'])
def query():
    print("arrived in python")
    # split into input (X) and output (Y) variables
    #X= numpy.array([[6,148,72,35,0,33.6,0.627,50]])
    #X = numpy.array([sys.argv[1].split(',')])
    #print("Request : ", request.form['input_x'].split(','))
    X = numpy.array([request.form['input_x'].split(',')])
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    #print("Loaded model from disk")
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    score = loaded_model.predict(X,verbose=0)
    #print("Score : ", score)
    score_ = score;
    return str(score);


if __name__ == "__main__":
    app.run()
