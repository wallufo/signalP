from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz,filtfilt 
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
import numpy as np

fs = 44100.0
T = 10
t = np.linspace(0, T, T*fs, endpoint=False)
x = 0.2*cos(2*pi*1000*t) + 0.3*sin(2*pi*2200*t+0.1) + \
        0.5*sin(2*pi*3400*t) + 0.6*sin(2*pi*4500*t + 0.1) + \
            0.7*sin(2*pi*6000*t+.8)
ffx = np.fft.fft(x)
ffx = np.abs(ffx)*2/T/fs 
ripple_db=60.0
width=500.0/fs
N, beta = kaiserord(ripple_db, width)
print(N,beta)
cutoffmin_hz=2000.0
cutoffmax_hz=5000.0
taps = firwin(N, [cutoffmin_hz/fs,cutoffmax_hz/fs], window=('kaiser', beta))
print(taps)
filtered_x = filtfilt(taps, 1.0, x)
ff = np.fft.fft(filtered_x)
f = np.linspace(0, fs, T*fs, endpoint=False) 
ff = np.abs(ff)*2/T/fs 
figure(1)
clf()
w, h = freqz(taps, worN=8000)
plot((w/pi)*fs, absolute(h), linewidth=2)
xlabel('Frequency (Hz)')
ylabel('Gain')
title('Frequency Response')
ylim(-0.05, 1.05)
grid(True)
figure(2)
plot(f,ffx)
figure(3)
plot(f,ff)
show()
