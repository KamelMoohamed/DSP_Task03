from scipy import signal
import numpy as np
import pickle
import os
import joblib
import librosa
from sklearn import preprocessing
from scipy.io.wavfile import read
from python_speech_features import mfcc


class Processing:
    def __init__(self):
        self.models1 = [
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Open The Door.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Open The Book.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Close The Window.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Open The Window.joblib")),
            joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Close The Door.joblib")),
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
        sentence = self.predict_model1(file)
        person = self.predict_model2(file)

        print(sentence)
        print(person)
            
        return sentence, person


    def predict_model2(self, file):
        audio, sr = librosa.load(file)
        vector = self.extract_features(audio, sr, nfft = 1200, winlen = 0.025)
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

        return self.process_output2(winner)


    def predict_model1(self, file):
        audio, sr = librosa.load(file)
        vector = self.extract_features(audio, 44100, nfft = 2205, winlen = 0.05)
        log_likelihood = np.zeros(len(self.models1))
        for i in range(len(self.models1)):
            gmm = self.models1[i] 
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()

        winner = np.argmax(log_likelihood)

        # flag = max(log_likelihood) - log_likelihood
        # testFlag = True
        # for i in range(len(flag)):
        #     if log_likelihood[i] == max(log_likelihood):
        #         continue
        #     if abs(flag[i]) < 0.7:
        #         testFlag = False

        print(log_likelihood)
        # print(flag)
        # if testFlag:
        #     winner = np.argmax(log_likelihood)
        # else:
        #     winner = 5

        if winner != 0:
            winner = 5

        return self.process_output1(winner)

    def predict_svm(self, file):
        x = list(self.features_extractor(file, n_samples = 46))
        x1 = list(self.features_extractor_lpc(file))
        x2 = self.features_extractor_rms(file)
        x3 = self.features_extractor_plp(file)
        sentenceModelInputs = x + x1
        sentenceModelInputs.append(x2)
        sentenceModelInputs.append(x3)

        sentenceModelInputs = np.array(sentenceModelInputs).reshape(1, -1)
        personsModelInputs = np.array(list(self.features_extractor(file, n_samples = 46))).reshape(1, -1)

        sentenceModelInputs = self.model1Scaler.transform(sentenceModelInputs)
        personsModelInputs = self.model2Scaler.transform(personsModelInputs)

        prediction1 = self.model1.predict(np.array(sentenceModelInputs))
        prediction2 = self.model2.predict(np.array(personsModelInputs))

        score = self.model1.predict_proba(np.array(sentenceModelInputs))
        if abs(score[0][0] - score[0][1]) < 0.2:
            sentence = self.process_output1(1)
        else:
            sentence = self.process_output1(prediction1[0])

        person = self.process_output2(prediction2[0])

        return sentence, person

    
    def process_output1(self, labelIndex):
        return ['Open The Door', 'Open The Book', 'Close The Window', \
            'Open The Window', 'Close The Door', 'Others'][labelIndex]

    def process_output2(self, labelIndex):
        return ["Kamel", "Abdelrahman", "Sama", "Yousr", "Others"][labelIndex]