from scipy.io import wavfile
import numpy as np

fs, signal = wavfile.read('song.wav')
WINDOW_SIZE = fs // 8

# colapse all the channels
signal = np.mean(signal, 1)
# Normalize to [-1, 1]
signal = signal / (np.max(np.abs(signal)))

# Make sure that our signal is of appropriate length to split into windows
signal = np.pad(signal, ((0, WINDOW_SIZE - (len(signal) % WINDOW_SIZE))), 'constant')

windows = np.array(np.split(signal, len(signal) // WINDOW_SIZE)).transpose()
