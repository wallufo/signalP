
import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np
import math 
from scipy.signal import butter, lfilter,buttord,freqs     
fs = 8000
dt = 1/fs
T = 10
t = np.linspace(0, T, T*fs, endpoint=False)
y = 5*np.sin(2*np.pi*t*500)+10*np.sin(2*np.pi*t*2500) 
N, Wn = buttord(np.pi*2*2000, np.pi*2*1000, 1, 20,True) 

wn=2*1000/fs 
b, a = butter(N,wn, 'high')
w,h=freqs(b,a)
filterY = lfilter(b, a, y)
f = np.linspace(0, fs, T*fs, endpoint=False) 
ff = np.fft.fft(y)
ff = np.abs(ff)*2/T/fs 
plt.figure()
plt.plot(f, ff)
plt.title('Before')
plt.show() 
ff = np.fft.fft(filterY)
ff = np.abs(ff)*2/T/fs 
plt.figure()
plt.plot(f, ff)
plt.title('After')
plt.show()
plt.figure()
plt.semilogx(w, 10 * np.log10(abs(h)))
plt.show()

