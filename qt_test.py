import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np
import math 
from scipy.signal import butter, lfilter,buttord,freqs   
b, a = signal.butter(5, 0.25, 'high', analog=True)
w, h = signal.freqs(b, a)
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.show()