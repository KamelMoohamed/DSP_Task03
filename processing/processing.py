from processing.Song import Song
import numpy as np
import pickle
import os
import joblib

class Processing:
    def __init__(self):
        print(os.path.dirname(os.path.abspath(__file__)))
        self.model1Scaler = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model1_scaler.bin"), 'rb'))
        self.model2Scaler = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scaler.joblib"))
        self.model1 = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model1.sav"), 'rb'))
        self.model2 = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model2.joblib"))
    
    def predict_pipelines(self, file):
        song = Song(file)
        lst1 = [song.max_pitch, song.avg_pitch, song.var_pitch, song.max_lpc, song.avg_lpc, song.var_lpc, 
                song.harmonic, song.harmonic_var, song.percussive, song.percussive_var, song.chromaAvg, 
                song.chromaVar, song.chroma_stft_mean, song.chroma_stft_var, song.chroma_cqt_mean, 
                song.chroma_cqt_var, song.Mfccs, song.Mfccs_var, song.mfcc_delta_mean, 
                song.mfcc_delta_var, song.Contrast, song.Contrast_var, song.Rolloff, song.Rolloff_var, 
                song.Zrate, song.Zrate_var, song.Cent, song.Cent_var, song.tonnetz_mean, song.tonnetz_var, 
                song.poly_features_mean, song.poly_features_var, song.spec_bw_mean, song.spec_bw_var, 
                song.rmse_mean, song.rmse_var]

        sentenceModelInputs = np.array(lst1).reshape(1,-1)
        personsModelInputs = np.array(lst1).reshape(1,-1)

        # sentenceModelInputs = self.model1Scaler.transform(sentenceModelInputs)
        personsModelInputs = self.model2Scaler.transform(personsModelInputs)

        # TODO: Predict with both models
        # prediction1 = self.model1.predict(np.array(sentenceModelInputs))
        prediction2 = self.model2.predict(np.array(personsModelInputs))
        
        # print(prediction1)
        print(prediction2)
        sentence = self.process_output1(0)
        personIndex = 0
        person = self.process_output2(prediction2[0])
        return sentence, person

    def process_output1(self, labelIndex):
        return ["Open", "Close", "Others"][labelIndex]

    def process_output2(self, labelIndex):
        return ["Kamel", "Abdelrahman", "Sama", "Yousr", "Others"][labelIndex]
