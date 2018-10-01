import numpy as np
from numpy import fft
from math import pi
from matplotlib import pyplot as plt
from data import signal, fs

def do_plot(t, fx, fs, i):
    hx = fft.rfft(fx)
    sample_points = np.linspace(0, fs / 2, len(hx))
    hx_norm = np.abs(hx)
    hx_norm = hx_norm / len(fx)

    plt.figure()

    plt.subplot(2, 1, 1)
    plt.plot(t, fx)
    plt.ylabel('f(t)')

    par1 = plt.subplot(2, 1, 2)
    par1.set_xlim(0, fs / 2)
    par1.set_xlabel("Frequency (Hz)")

    par2 = par1.twinx()

    par1.set_ylim(0, 180)
    par1.set_ylabel("angle(dft(f))")
    par2.set_ylim(0, np.max(hx_norm) * 1.1)
    par2.set_ylabel("mag(dft(f))")

    p1, = par1.plot(
        sample_points,
        np.abs(np.angle(hx, deg=True)),
        color=plt.cm.viridis(0.5),
        label='angle(dft(f))'
    )
    p2, = par2.plot(
        sample_points,
        hx_norm,
        color=plt.cm.viridis(0),
        label='mag(dft(f))'
    )

    par1.legend(handles=[p1, p2], loc='best')

    plt.savefig('img/sin' + str(i) + '.png', bbox_inches='tight')

# Generate 1000 time values, evenly spaced from 0 to 4 seconds
t = np.linspace(0, 4, 1000)
fx = np.sin(t * 2 * pi)
do_plot(t, fx, 1000 / 4, 0)

fx = np.zeros(t.shape)
for i in range(0, t.shape[0] // 50):
    fx[i*50:(i+1)*50] = (i % 2) * 2 - 1

do_plot(t, fx, 1000 / 4,  1)

do_plot(np.linspace(0, (len(signal) / fs), len(signal)), signal, fs, 2)
