from data import windows, signal, WINDOW_SIZE, fs
from matplotlib import pyplot as plt
from matplotlib import transforms
from matplotlib.gridspec import GridSpec
from numpy import fft
from waterfall_plot import plot_waterfall
import numpy as np

spectral_content = fft.rfft(windows, axis=0)
normed_spectral_content = np.abs(spectral_content)
sample_size = (WINDOW_SIZE // 2) + ((WINDOW_SIZE + 1) % 2)
freq_scaling = np.linspace(0, fs / 2, normed_spectral_content.shape[0])
freq_scaling = freq_scaling.reshape((sample_size, 1))

pl = np.log(freq_scaling * normed_spectral_content + 0.0001)

# Summarize data
# Our buckets will be roughly:
# 0 - 100 Hz
# 101 - 2 Khz
# 2Khz - 20Khz
div1 = int(sample_size * (100 / (fs * 2)))
div2 = int(sample_size * (2000 / (fs * 2)))

SEG_START = 100
SEG_END = 300

def sumarize(start, stop):
    # Select the right part of the array
    tr = np.sum(pl[start:stop,SEG_START:SEG_END], axis=0)
    # Compute a moving average (window size = 16)
    # to smooth out measurements
    MA_SIZE = 3
    tr = np.cumsum(tr)
    tr[MA_SIZE:] = tr[MA_SIZE:] - tr[:-MA_SIZE]
    tr = tr[MA_SIZE-1:] / MA_SIZE
    # Normalize the moving average
    mi = np.min(tr)
    ma = np.max(tr)
    # Normalize TR
    tr = (tr - mi) / (ma - mi)
    return tr

sum0 = sumarize(0, div1)
sum1 = sumarize(div1, div2)
sum2 = sumarize(div2, -1)

fig = plt.figure(figsize=(8,16))

subplots = fig.subplots(ncols=1, nrows=4, sharex='col')

p0 = subplots[0].plot(sum0)
subplots[0].set_title('lows')
subplots[0].axhline(y=0.75)
p1 = subplots[1].plot(sum1)
subplots[1].set_title('mids')
subplots[1].axhline(y=0.8)
p2 = subplots[2].plot(sum2)
subplots[2].set_title('his')
subplots[2].axhline(y=0.6)

subplots[3].imshow(pl[:,SEG_START:SEG_END], aspect='auto')

plt.savefig('img/beats.png', bbox_inches='tight', dpi=fig.dpi)
