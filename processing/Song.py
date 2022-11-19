import numpy as np
from scipy import signal

import librosa
import librosa.display as DSP
from tempfile import mktemp
from PIL import Image
import imagehash

import pylab

class Song(object):
    def __init__(self, file):
        wavdata, samplingFrequency = librosa.load(file)
        self.wavdata,self.samplingFrequency = wavdata, samplingFrequency
        
        y_harmonic, y_percussive = librosa.effects.hpss(wavdata)
        self.y_harmonic, self.y_percussive = y_harmonic, y_percussive
        
        self.spectrogram = self.getSpectrogram()
        
        # Harmonic
        self.harmonic = np.mean(y_harmonic)
        self.harmonic_var = np.var(y_harmonic)
        
        # Precussive
        self.percussive = np.mean(y_percussive)
        self.percussive_var = np.var(y_percussive)
        
        # Pitches
        pitches, magnitudes = librosa.core.piptrack(y = wavdata , sr = samplingFrequency)
        self.max_pitch = np.max(pitches)
        self.avg_pitch = np.mean(pitches)
        self.var_pitch = np.var(pitches)
        
        # LPC Calculations
        spectral_lpc = librosa.lpc(wavdata, order=2)
        self.max_lpc = np.max(spectral_lpc)
        self.avg_lpc = np.mean(spectral_lpc)
        self.var_lpc = np.var(spectral_lpc)
        
        # Chroma
        chroma = librosa.feature.chroma_cens(y=y_harmonic, sr=samplingFrequency)
        self.chromaAvg = np.mean(chroma)
        self.chromaVar = np.var(chroma)
        
        chroma_stft = librosa.feature.chroma_stft(y=y_harmonic, sr=samplingFrequency)
        self.chroma_stft_mean = np.mean(chroma_stft)
        self.chroma_stft_var = np.var(chroma_stft)

        chroma_cqt = librosa.feature.chroma_cqt(y=y_harmonic, sr=samplingFrequency)
        self.chroma_cqt_mean = np.mean(chroma_cqt)
        self.chroma_cqt_var = np.var(chroma_cqt)
        
        # MFCC
        mfccs = librosa.feature.mfcc(y=y_harmonic, sr=samplingFrequency)
        self.Mfccs = np.mean(mfccs)
        self.Mfccs_var = np.var(mfccs)
        
        delta = librosa.feature.delta(mfccs)
        self.mfcc_delta_mean = np.mean(delta)
        self.mfcc_delta_var = np.var(delta)
        
        # Contrast
        contrast = librosa.feature.spectral_contrast(y=y_harmonic,sr=samplingFrequency)
        self.Contrast = np.mean(contrast)
        self.Contrast_var = np.var(contrast)
        
        # Rolloff
        rolloff = librosa.feature.spectral_rolloff(y=wavdata, sr=samplingFrequency)
        self.Rolloff = np.mean(rolloff)
        self.Rolloff_var = np.var(rolloff)

        # Z-rate
        zrate = librosa.feature.zero_crossing_rate(y_harmonic)
        self.Zrate = np.mean(zrate)
        self.Zrate_var = np.var(zrate)

        # Centroid
        cent = librosa.feature.spectral_centroid(y=wavdata, sr=samplingFrequency)
        self.Cent = np.mean(cent)
        self.Cent_var = np.var(cent)

        tonnetz = librosa.feature.tonnetz(y=wavdata, sr=samplingFrequency)
        self.tonnetz_mean = np.mean(tonnetz)
        self.tonnetz_var = np.var(tonnetz)
        
        # Poly
        poly_features = librosa.feature.poly_features(S=self.spectrogram, sr=samplingFrequency)
        self.poly_features_mean = np.mean(poly_features)
        self.poly_features_var = np.var(poly_features)
        
        # Bandwidth
        spec_bw = librosa.feature.spectral_bandwidth(y=wavdata, sr=samplingFrequency)
        self.spec_bw_mean = np.mean(spec_bw)
        self.spec_bw_var = np.var(spec_bw)
        
        # RMSE
        rmse = librosa.feature.rms(y=wavdata)
        self.rmse_mean = np.mean(rmse)
        self.rmse_var = np.var(rmse)
        
        # Melspectogram
        melspectrogram = librosa.feature.melspectrogram(y=wavdata, sr=samplingFrequency)
        self.melspec_mean = np.mean(melspectrogram)
        self.melspec_var = np.var(melspectrogram)

        
    # Features with Hashing
    def getSpectrogram(self):
        f, t, Sxx = signal.spectrogram(self.wavdata, 44100)
        return Sxx

    def getHashedSpectrogram(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        librosa.display.specshow(librosa.amplitude_to_db(self.spectrogram, ref=np.max), y_axis='linear')
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)

    def getFeature_centroid(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_centroids = librosa.feature.spectral_centroid(S = self.spectrogram, sr = self.samplingFrequency)
        DSP.specshow(spectral_centroids)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)

    def getFeature_rolloff(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_rolloffs = librosa.feature.spectral_rolloff(S = self.spectrogram, sr = self.samplingFrequency)
        librosa.display.specshow(spectral_rolloffs)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)

    def getFeature_chroma(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_chroma = librosa.feature.chroma_stft(y=self.y_harmonic, sr = self.samplingFrequency)
        librosa.display.specshow(spectral_chroma)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)
    
    def getFeature_chroma_cqt(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_chroma_cqt = librosa.feature.chroma_cqt(y=self.y_harmonic, sr=self.samplingFrequency)
        librosa.display.specshow(spectral_chroma_cqt)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)
    
    def getFeature_mfcc(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_mfcc = librosa.feature.mfcc(y = self.y_harmonic, sr = self.samplingFrequency)
        librosa.display.specshow(spectral_mfcc)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)
    
    def getFeature_mels_spectorgram(self):
        outputFile = mktemp('.png')  # use temporary file
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        spectral_melspectrogram = librosa.feature.melspectrogram(S = self.spectrogram, sr = self.samplingFrequency)
        librosa.display.specshow(spectral_melspectrogram)
        pylab.savefig(outputFile, bbox_inches=None, pad_inches=0)
        pylab.close()
        return int(str(imagehash.phash(Image.open(outputFile))), 16)
    