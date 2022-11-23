from processing.Song import Song
import numpy as np
import pickle
import os
import joblib
import librosa

class Processing:
    def __init__(self):
        print(os.path.dirname(os.path.abspath(__file__)))
        self.model1Scaler = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scaler1.joblib"))
        self.model2Scaler = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scaler2.joblib"))
        self.model1 = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model1.joblib"))
        self.model2 = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "model2.joblib"))
    
    def features_extractor(self, file):
        audio, sample_rate = librosa.load(file, res_type='kaiser_fast') 
        mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    
        return mfccs_scaled_features

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
        personsModelInputs = np.array(self.features_extractor(file)).reshape(1, -1)

        sentenceModelInputs = self.model1Scaler.transform(sentenceModelInputs)
        personsModelInputs = self.model2Scaler.transform(personsModelInputs)

        prediction1 = self.model1.predict(np.array(sentenceModelInputs))
        prediction2 = self.model2.predict(np.array(personsModelInputs))

        sentence = self.process_output1(prediction1[0])
        personIndex = 0
        person = self.process_output2(prediction2[0])
        return sentence, person

    def process_output1(self, labelIndex):
        return ["Open", "Close", "Others"][labelIndex]

    def process_output2(self, labelIndex):
        return ["Abdelrahman", "Kamel", "Sama", "Yousr", "Others"][labelIndex]
