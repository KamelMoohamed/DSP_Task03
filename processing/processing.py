from scipy import signal
import numpy as np
import os
import joblib
import librosa
from processing.feature_extraction_processing import extract_features


class Processing:
    def __init__(self):
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models_files")

        self.labels1 = ["Open The Door", "Close The Door", "Open The Window", \
                        "Close The Window", "Open The Book", "Others"]
        self.labels2 = ["Kamel", "Abdelrahman", "Sama", "Yousr", "Others"]

        self.models1 = [ 
            joblib.load(os.path.join(base_path, label + ".joblib")) for label in self.labels1
        ]
        self.models2 = [ 
            joblib.load(os.path.join(base_path, label + ".joblib")) for label in self.labels2[:4]
        ]


    def prediction_pipelines(self, file):
        audio, sampleRate = librosa.load(file)

        sentence = self.predict_model1(audio, sampleRate)
        person = self.predict_model2(audio, sampleRate)

        # Empty Records Condition
        duration = librosa.get_duration(y=audio, sr=sampleRate)
        if(duration < 1):
            return 'Others', 'Others'

        return sentence, person


    def predict_model1(self, audio, sampleRate):
        # Extract Features
        vector = extract_features(audio, 44100, nfft = 2205, winlen = 0.05)
        outcomePossibility = np.zeros(len(self.models1))
        for i in range(len(self.models1)):
            gmm = self.models1[i] 
            scores = np.array(gmm.score(vector))
            outcomePossibility[i] = scores.sum()

        winner = np.argmax(outcomePossibility)

        normalizedPossibility = max(outcomePossibility) - outcomePossibility
        othersFlag = True
        for i in range(len(normalizedPossibility)):
            if outcomePossibility[i] == max(outcomePossibility):
                continue
            if abs(normalizedPossibility[i]) < 0.3:
                othersFlag = False
        if othersFlag:
            winner = np.argmax(outcomePossibility)
        else:
            winner = 5

        self.yAxis1 = [outcomePossibility[0], max(outcomePossibility[1:])]

        # Normalized the output to two labels only (open the door, others)
        if winner != 0:
            winner = 5

        # Get The String Labels
        return self.process_output1(winner)

    def predict_model2(self, audio, sampleRate):
        # Extract Features
        vector = extract_features(audio, sampleRate, nfft = 2205, winlen = 0.05)
        outcomePossibility = np.zeros(len(self.models2))

        # Looping through the models
        for i in range(len(self.models2)):
            # model prediction
            gmm = self.models2[i] 
            scores = np.array(gmm.score(vector))
            outcomePossibility[i] = scores.sum()

        normalizedPossibility = max(outcomePossibility) - outcomePossibility
        othersFlag = True
        for i in range(len(normalizedPossibility)):
            if outcomePossibility[i] == max(outcomePossibility):
                continue
            if abs(normalizedPossibility[i]) < 0.7:
                othersFlag = False
        
        # Others Condition
        if othersFlag:
            winner = np.argmax(outcomePossibility)
        else:
            winner = 4

        self.yAxis2 = outcomePossibility

        # Get The String Labels
        return self.process_output2(winner)

    def process_output1(self, labelIndex):
        return self.labels1[labelIndex]

    def process_output2(self, labelIndex):
        print(labelIndex)
        self.output2 = self.labels2[labelIndex]
        return self.output2

    def getGraph1Data(self):
        yAxis = self.yAxis1
        for i in range(len(yAxis)):
            yAxis[i] = 2**yAxis[i]
        yAxis = yAxis / sum(yAxis)
        return ['Open The Door', 'Others'], list(yAxis*100)

    def getGraph2Data(self):
        yAxis = self.yAxis2
        for i in range(len(yAxis)):
            yAxis[i] = 2**yAxis[i]
        yAxis = yAxis / sum(yAxis)
        return self.labels2, list(yAxis*100)

    def getGraph1Line(self):
        yAxis = list(self.yAxis1)
        flagY = list(self.yAxis1)

        flagY.remove(max(flagY))
        maxValue = max(flagY) + 0.3
        yAxis[yAxis.index(max(flagY))] = maxValue
        
        lst = []
        for i in range(len(yAxis)):
            lst.append(2**yAxis[i])
        yAxis.remove(max(yAxis))
        return ((2**maxValue)/sum(lst))*100


    def getGraph2Line(self):
        yAxis = list(self.yAxis2)
        flagY = list(self.yAxis2)

        flagY.remove(max(flagY))
        maxValue = max(flagY) + 0.7
        yAxis[yAxis.index(max(flagY))] = maxValue
        
        lst = []
        for i in range(len(yAxis)):
            lst.append(2**yAxis[i])
        yAxis.remove(max(yAxis))
        return ((2**maxValue)/sum(lst))*100

    def getSpectrogramFilePath(self):
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "records_files")
        return os.path.join(base_path, self.output2 + '.wav')