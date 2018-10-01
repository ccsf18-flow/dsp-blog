from data import windows, signal, WINDOW_SIZE, fs
from matplotlib import pyplot as plt
from matplotlib import transforms
from matplotlib.gridspec import GridSpec
from numpy import fft
from waterfall_plot import plot_waterfall
import numpy as np

# Start by showing the signal itself
# plt.plot(signal)
# plt.show()

# Show the raw spectral content
spectral_content = fft.rfft(windows, axis=0)
normed_spectral_content = np.abs(spectral_content)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(1, 1, 1);

ax_im = ax.imshow(normed_spectral_content, aspect='auto')
ax.autoscale(False)
ax.set_ylim((0, spectral_content.shape[0]))
ax.set_xlim((0, spectral_content.shape[1]))

plt.savefig('img/norm.freqs.png', bbox_inches='tight', dpi=fig.dpi)

# And show it with some slices
x_slice = 122
y_slices = [100, 500, 2500]

plot_waterfall(normed_spectral_content, x_slice, y_slices, 'img/sliced.norm.freqs.png')

# Perceptually linearzize the spectrum
sample_size = (WINDOW_SIZE // 2) + ((WINDOW_SIZE + 1) % 2)
# Energy scales linearly with frequency
freq_scaling = np.linspace(0, fs / 2, normed_spectral_content.shape[0])
# Magic to make numpy happy
freq_scaling = freq_scaling.reshape((sample_size, 1))
# "Perceptually linear" version: log of the incoming energy
# We also add a tiny offset, just to avoid dealing with entries
# that have zero energy
pl = np.log(freq_scaling * normed_spectral_content + 0.0001)
plot_waterfall(pl, x_slice, y_slices, 'img/sliced.norm.pl.png', show_angles=False)

plot_waterfall(pl[:,100:300], x_slice, y_slices, 'img/sliced.norm.pl.focused.png', show_angles=False)
