import numpy as np
import matplotlib.pyplot as plt
t=np.linspace(-10.0,10.0,0,1000)
def sinSignal(A,w,t,phi):
    return A*np.cos(w*t+phi)