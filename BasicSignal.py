import numpy as np
import matplotlib.pyplot as plt
t=np.linspace(0,10.0,1000)
n=np.arange(0,15)
A=1.0
w=2.0
phi=3.0
a=0.5
def CosSignal(A,w,t,phi):
    return A*np.cos(w*t+phi)
def ExpSignal(A,a):
    return A*np.exp(a*t)
plt.subplot(221)
plt.title(u'$A*cos(w*t+phi)$')
plt.plot(t,CosSignal(A,w,t,phi))
plt.subplot(222)
plt.title(u'$A*e^t$')
plt.plot(t,ExpSignal(A,a))
plt.subplot(223)
plt.title(u'$A*cos(w*n+phi)$')
plt.stem(n,np.cos(n*np.pi/6))
plt.subplot(224)
plt.title(u'$A*e^n$')
plt.stem(n,A*np.exp(a*n))
plt.show()
