from scipy import signal
import numpy as np
import os
import joblib
import librosa
from sklearn import preprocessing
from python_speech_features import mfcc


class Processing:
    def __init__(self):
        self.models1 = [
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Open The Door.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Close The Door.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Open The Window.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Close The Window.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Open The Book.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Others.joblib"))
        ]
        self.models2 = [
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Kamel.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Abdelrahman.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sama.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Yousr.joblib"))
        ]


    def calculate_delta(self, array):
        rows, cols = array.shape
        deltas = np.zeros((rows,20))
        N = 2
        for i in range(rows):
            index = []
            j = 1
            while j <= N:
                if i-j < 0:
                    first =0
                else:
                    first = i-j
                if i+j > rows-1:
                    second = rows-1
                else:
                    second = i+j 
                index.append((second,first))
                j+=1
            deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
        return deltas


    def extract_features(self, audio, rate, nfft, winlen):
        mfcc_feature = mfcc(audio,rate, winlen, 0.01, 20, nfft = nfft, appendEnergy = True)
        mfcc_feature = preprocessing.scale(mfcc_feature)
        delta = self.calculate_delta(mfcc_feature)
        combined = np.hstack((mfcc_feature, delta)) 
        return combined
    
    def predict_pipelines(self, file):
        audio, sr = librosa.load(file)
        duration = librosa.get_duration(y=audio, sr=sr)

        sentence = self.predict_model1(file)
        person = self.predict_model2(file)

        print(sentence)
        print(person)
        if(duration < 1):
            return 'Others', 'Others'
            
        return sentence, person


    def predict_model1(self, file):
        audio, sr = librosa.load(file)
        vector = self.extract_features(audio, 44100, nfft = 2205, winlen = 0.05)
        log_likelihood = np.zeros(len(self.models1))
        for i in range(len(self.models1)):
            gmm = self.models1[i] 
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()

        winner = np.argmax(log_likelihood)

        print(log_likelihood)
        flag = max(log_likelihood) - log_likelihood
        print(flag)
        testFlag = True
        for i in range(len(flag)):
            if log_likelihood[i] == max(log_likelihood):
                continue
            if abs(flag[i]) < 0.3:
                testFlag = False
        if testFlag:
            winner = np.argmax(log_likelihood)
        else:
            winner = 5

        self.yAxis1 = [log_likelihood[0], max(log_likelihood[1:])]

        if winner != 0:
            winner = 5

        return self.process_output1(winner)

    def predict_model2(self, file):
        audio, sr = librosa.load(file)
        vector = self.extract_features(audio, sr, nfft = 2205, winlen = 0.05)
        log_likelihood = np.zeros(len(self.models2))
        for i in range(len(self.models2)):
            gmm = self.models2[i] 
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()

        flag = max(log_likelihood) - log_likelihood
        testFlag = True
        for i in range(len(flag)):
            if log_likelihood[i] == max(log_likelihood):
                continue
            if abs(flag[i]) < 0.7:
                testFlag = False
        if testFlag:
            winner = np.argmax(log_likelihood)
        else:
            winner = 4

        self.yAxis2 = log_likelihood

        return self.process_output2(winner)

    
    def process_output1(self, labelIndex):
        return ['Open The Door', 'Close The Door', 'Open The Window', 'Close The Window',\
             'Open The Book', 'Others'][labelIndex]

    def process_output2(self, labelIndex):
        return ["Kamel", "Abdelrahman", "Sama", "Yousr", "Others"][labelIndex]


    def getGraph1Data(self):
        x = self.yAxis1
        print(x)
        for i in range(len(x)):
            x[i] = 2**x[i]
        x = x / sum(x)
        return ['Open The Door', 'Others'], list(x*100)

    def getGraph2Data(self):
        x = self.yAxis2
        print(x)
        for i in range(len(x)):
            x[i] = 2**x[i]
        x = x / sum(x)
        return ['Kamel', 'Abdelrahman', 'Sama', 'Yousr'], list(x*100)



    def getSpectrogram1(self, file):
        audio, sr = librosa.load(file)
        f, t, Sxx = signal.spectrogram(audio, sr)
        return f, t, Sxx

    def getSpectrogram2(self, file):
        audio, sr = librosa.load(file)
        f, t, Sxx = signal.spectrogram(audio, sr)
        return f, t, Sxx
        