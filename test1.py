import numpy as np
import matplotlib.pyplot as plt
t = np.linspace(-10.0,10.0,1000)  #通过linspace函数指定t的取值范围
A=5.0
w=5.0
phi=1/3
real=1.0
image=3.0
def expSignal(A,t):
    return np.exp(A*t)
def sincSignal(A,t):
    return np.sinc(A*t/np.pi)
def sinSignal(A,w,t,phi):
    return A*np.sin(w*t+phi)
def triangle_wave(x, c, hc):  # 幅度为hc，宽度为c,斜度为hc/2c的三角波
    if x >= c / 2:
        r = 0.0
    elif x <= -c / 2:
        r = 0.0
    elif x > -c / 2 and x < 0:
        r = 2 * x / c * hc + hc
    else:
        r = -2 * x / c * hc + hc
    return r
def complexSignal(real,image,t):
    return np.exp(complex(real,image)*t)
def unit(t):
    r = np.where(t > 0.0, 1.0, 0.0)
    return r
plt.subplot(511)
plt.plot(t,sincSignal(A,t))
plt.subplot(512)
plt.plot(t,sinSignal(A,w,t,phi))
y=np.array([triangle_wave(x,4.0,2.0) for x in t])
plt.subplot(513)
plt.plot(t,y)
plt.subplot(514)
plt.plot(t,y)
plt.subplot(514)
plt.plot(t,np.imag(complexSignal(real,image,t)))
plt.subplot(515)
plt.plot(t,t*unit(t))
plt.show()