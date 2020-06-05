import sounddevice as sd
from scipy.io.wavfile import write
import os
import pickle
import librosa
import numpy as np
import os
import math
from sklearn.cluster import KMeans
import hmmlearn.hmm

from tkinter import *
import time
##############################################

fs = 48000   # Sample rate
seconds = 150  # Max of recording
gui = Tk(className='Word Recognition') # define tkinter
# set window size
gui.geometry("300x150")
gui.configure(bg="black") #dark theme


models={}

cname = "co_the"
pkl_filename = 'co_the_model.pkl'
# Loading the saved model pickle
model_pkl = open(pkl_filename, 'rb')
model = pickle.load(model_pkl)
models[cname] = model

cname = "khong"
pkl_filename = 'khong_model.pkl'
# Loading the saved model pickle
model_pkl = open(pkl_filename, 'rb')
model = pickle.load(model_pkl)
models[cname] = model

cname = "nguoi"
pkl_filename = 'nguoi_model.pkl'
# Loading the saved model pickle
model_pkl = open(pkl_filename, 'rb')
model = pickle.load(model_pkl)
models[cname] = model

cname = "toi"
pkl_filename = 'toi_model.pkl'
# Loading the saved model pickle
model_pkl = open(pkl_filename, 'rb')
model = pickle.load(model_pkl)
models[cname] = model

cname = "nay"
pkl_filename = 'nay_model.pkl'
# Loading the saved model pickle
model_pkl = open(pkl_filename, 'rb')
model = pickle.load(model_pkl)
models[cname] = model
print ("Done loading")







startTime = 0
# function to record
def get_mfcc(file_path):
    y, sr = librosa.load(file_path, duration=5.0) # read .wav file
    hop_length = math.floor(sr*0.010) # 10ms hop
    win_length = math.floor(sr*0.025) # 25ms frame
    # mfcc is 12 x T matrix
    mfcc = librosa.feature.mfcc(
        y, sr, n_mfcc=12, n_fft=1024,
        hop_length=hop_length)
        #hop_length=hop_length, win_length=win_length)
    # substract mean from mfcc --> normalize mfcc
    mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1,1)) 
    # delta feature 1st order and 2nd order
    delta1 = librosa.feature.delta(mfcc, order=1)
    delta2 = librosa.feature.delta(mfcc, order=2)
    # X is 36 x T
    X = np.concatenate([mfcc, delta1, delta2], axis=0) # O^r
    # return T x 36 (transpose of X)
    return X.T # hmmlearn use T x N matrix


def get_class_data(data_dir):
    files = os.listdir(data_dir)
    mfcc = [get_mfcc(os.path.join(data_dir,f)) for f in files if f.endswith(".wav")]
    return mfcc


def clustering(X, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, n_init=50, random_state=0, verbose=0)
    kmeans.fit(X)
    print("centers", kmeans.cluster_centers_.shape)
    return kmeans


def Rec_sentence():

    global startTime
    startTime = time.time()
    print("start recording")
    global myrecording
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

    return startTime
        
btnStart = Button(gui, text = 'Start', command = Rec_sentence) #start record button
btnStart.pack()
# function to save 
def Stop_rec():
    sd.stop()
    print("finish")
    duration = time.time() - startTime
    frame = int(duration * fs)
    write('./BT2/test/predict'+'.' + 'wav', fs, myrecording[:frame])  # Save as WAV file


def predict():
    class_names = ["test"]
    dataset = {}
    for cname in class_names:
        dataset[cname] = get_class_data(os.path.join("./BT2/", cname))
    all_vectors = np.concatenate([np.concatenate(v, axis=0) for k, v in dataset.items()], axis=0)
    #kmeans = clustering(all_vectors)

    for cname in class_names:
        class_vectors = dataset[cname]
        dataset[cname] = list([kmeans.predict(v).reshape(-1,1) for v in dataset[cname]])
        X = np.concatenate(dataset[cname])
        lengths = list([len(x) for x in dataset[cname]])

    for true_cname in class_names:

        for O in dataset[true_cname]:
            score = {cname : model.score(O, [len(O)]) for cname, model in models.items() if cname[:4] != 'test' }
            max_value = max(score.values())
            max_key =[k for k, v in score.items() if v == max_value]
            max_key = str(max_key)
            max_key = max_key.split("'")[1]
            print(max_key)
    
btnStop = Button(gui, text = 'Stop', command = Stop_rec) #stop record button
btnStop.pack()

btnPredict = Button(gui, text = 'Predict', command = predict) #predict
btnPredict.pack()

gui.mainloop()



   
