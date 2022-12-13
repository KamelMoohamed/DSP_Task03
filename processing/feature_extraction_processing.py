from scipy import signal
import numpy as np
import librosa
from sklearn import preprocessing
from python_speech_features import mfcc
import pandas as pd
import os

def calculate_delta(array):
    rows, cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows-1:
                second = rows-1
            else:
                second = i+j 
            index.append((second, first))
            j+=1
        deltas[i] = (array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

def extract_features(audio, sampleRate, nfft, winlen):
    mfcc_feature = mfcc(audio, sampleRate, winlen, 0.01, 20, nfft = nfft, appendEnergy = True)
    mfcc_feature = preprocessing.scale(mfcc_feature)
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature, delta)) 
    return combined

def getSpectrogram(file):
    audio, sampleRate = librosa.load(file)
    freq, time, freqAmp = signal.spectrogram(audio, sampleRate)
    freqAmp[freqAmp < 0.00000001] = 0.00000001
    freqAmp = 10*np.log10(freqAmp)
    return freq, time, freqAmp

def features_extractor(file):
    audio, sample_rate = librosa.load(file, res_type='kaiser_fast') 
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=46)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    
    return mfccs_scaled_features

def getGraph3Data(file):
    newRow = list(features_extractor(file))
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model1.csv'))
    df[df['y'] != 0] = 1
    newRow.append(2)
    print(len(newRow))
    df.iloc[0,:] = newRow
    return df.iloc[:,0].values.tolist(), df.iloc[:,1].values.tolist(), df['y'].values.tolist()


def getGraph4Data(file):
    newRow = list(features_extractor(file))
    newRow.append(4)
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model2.csv'))
    print(len(newRow))
    df.iloc[0,:] = newRow
    return df.iloc[:,0].values.tolist(), df.iloc[:,27].values.tolist(), df['y'].values.tolist()
