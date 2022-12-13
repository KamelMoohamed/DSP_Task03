import librosa
import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)

IDX_FREQ_I = 0
IDX_TIME_J = 1
DEFAULT_WINDOW_SIZE = 4096
DEFAULT_OVERLAP_RATIO = 0.5
DEFAULT_FAN_OUT_VALUE = 10
DEFAULT_AMP_MIN = 10
PEAK_NEIGHBORHOOD_SIZE = 20
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200
PEAK_SORT = True
FINGERPRINT_REDUCTION = 20
DEFAULT_FS = 44100


def fingerprint(file, Fs=DEFAULT_FS,
                wsize=DEFAULT_WINDOW_SIZE,
                wratio=DEFAULT_OVERLAP_RATIO,
                fan_value=DEFAULT_FAN_OUT_VALUE,
                amp_min=DEFAULT_AMP_MIN, plot=False):

    channel_samples, sampleRate = librosa.load(file)

    arr2D = librosa.stft(channel_samples, n_fft = wsize, hop_length=int(wsize * wratio))
    arr2D = librosa.amplitude_to_db(np.abs(arr2D))

    frequency_idx, time_idx = get_2D_peaks(arr2D, amp_min = amp_min)
    return frequency_idx, time_idx


def get_2D_peaks(arr2D, amp_min=DEFAULT_AMP_MIN):
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our filter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood,
                                       border_value=1)

    detected_peaks = local_max ^ eroded_background

    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = filter(lambda x: x[2] > amp_min, peaks)  # freq, time, amp

    frequency_idx = []
    time_idx = []
    for x in peaks_filtered:
        frequency_idx.append(x[1])
        time_idx.append(x[0])

    return frequency_idx, time_idx