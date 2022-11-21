from processing.Song import Song
import numpy as np
import pickle

class Processing:
    def __init__(self):
        self.model1Scaler = pickle.load(open("model1_scaler.bin", 'rb'))
        self.model1Scaler = pickle.load(open("model2_scaler.bin", 'rb'))
        self.model1 = pickle.load(open("model1.sav", 'rb'))
        self.model2 = pickle.load(open("model2.sav", 'rb'))
    
    def predict_pipelines(self, file):
        song = Song(file)
        lst1 = [song.max_pitch, song.avg_pitch, song.var_pitch, song.max_lpc, song.avg_lpc, song.var_lpc, 
                song.harmonic, song.harmonic_var, song.percussive, song.percussive_var, song.chromaAvg, 
                song.chromaVar, song.chroma_stft_mean, song.chroma_stft_var, song.chroma_cqt_mean, 
                song.chroma_cqt_var, song.Mfccs, song.Mfccs_var, song.mfcc_delta_mean, 
                song.mfcc_delta_var, song.Contrast, song.Contrast_var, song.Rolloff, song.Rolloff_var, 
                song.Zrate, song.Zrate_var, song.Cent, song.Cent_var, song.tonnetz_mean, song.tonnetz_var, 
                song.poly_features_mean, song.poly_features_var, song.spec_bw_mean, song.spec_bw_var, 
                song.rmse_mean, song.rmse_var, song.getFeature_chroma(), song.getFeature_mfcc(), 
                song.getFeature_mels_spectorgram()]

        sentenceModelInputs = np.array(lst1)
        personsModelInputs = np.array(lst1)

        sentenceModelInputs = self.model1Scaler(sentenceModelInputs)
        personsModelInputs = self.model1Scaler(personsModelInputs)

        # TODO: Predict with both models
        sentence = self.process_output1(self.model1.predict(sentenceModelInputs))
        personIndex = 0
        person = self.process_output2(personIndex)
        return sentence, person

    def process_output1(self, labelIndex):
        return ["Open", "Close", "Others"][labelIndex]

    def process_output2(self, labelIndex):
        return ["Kamel", "Abdelrahman", "Sama", "Yousr", "Others"][labelIndex]
