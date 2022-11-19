from processing.Song import Song
import numpy as np

class Processing:
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

        # TODO: Scale the input with Standard Scaler
        # TODO: Predict with both models
        isOpen = True
        personIndex = 0
        person = self.process_output(personIndex)
        return isOpen, person

    def process_output(self, labelIndex):
        return ["Kamel", "Abdelrahman", "Sama", "Yousr", "Others"][labelIndex]
