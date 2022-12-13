from scipy import signal
import numpy as np
import librosa
from sklearn import preprocessing
from python_speech_features import mfcc

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
    return freq, time, freqAmp