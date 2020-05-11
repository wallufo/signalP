#import
import os
import wave as we
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import math
def goertzel(simple,freq_indices,N):
    w=[]
    c=[]
    p=[]
    for i in range(0,8):
        w.append(2*np.pi*freq_indices[i]/N)
        wc=w[i]
        ans=2*np.cos(wc)
        c.append(ans)
    q1=q2=0
    for i in range(0,8):
        for j in range(0,N):
            q0=c[i]*q1-q2+simple[j]
            q2=q1
            q1=q0
        ans=q1*q1+q2*q2-c[i]*q1*q2
        p.append(ans)
        q1=q2=0
    return p
def findIndex(simple):
    for i in range(0,3):
        if simple[i]==max(simple):
            index=i
            break
    return index
path='e:\\signalP\\'
filepath=os.listdir(path)
print(filepath[9])
f=we.open(path+filepath[9],'rb')
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
strData = f.readframes(nframes)#读取音频，字符串格式
waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int
waveData = waveData*1.0/(max(abs(waveData)))#wave幅值归一化
f.close()
time = np.arange(0,nframes)*(1.0 / framerate)
# plt.plot(time,waveData)
# plt.xlabel("Time(s)")
# plt.ylabel("Amplitude")
# plt.title("Single channel wavedata")
# plt.show()
f=[697,770,852,941,1209,1336,1477,1633]
N=8000
i=0
k=0
j=0
fs=8000
xk=[]
num=[]
freq_indices=[]
tm=np.array([[1,2,3,65],[4,5,6,66],[7,8,9,67],[42,0,35,68]])
limit=0.5*max(waveData)
datalength=len(time)
for fi in f:
    freq_indices.append(int(fi/fs*N))
for i in range(0,datalength):
    if j>=11:
        break
    if np.abs(waveData[k])>limit :
        x1=waveData[k:k+N]
        xk=goertzel(x1,freq_indices,N)
        num.append(findIndex(xk[0:3]))
        num.append(findIndex(xk[4:7]))
        print(tm[num[j*2],num[j*2+1]])
        k=k+N
        j=j+1
    else:
        k=k+1

