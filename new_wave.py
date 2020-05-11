import wave
import numpy as np
import struct
import matplotlib.pyplot as plt
fl=[697,770,852,941] #低频频率
fh=[1209,1336,1477,1633] #高频频率
Tmf={'1':[fl[0],fh[0]],'2':[fl[0],fh[1]],'3':[fl[0],fh[2]],'A':[fl[0],fh[3]],'4':[fl[1],fh[0]],'5':[fl[1],fh[1]],'6':[fl[1],fh[2]],'B':[fl[1],fh[3]],'7':[fl[2],fh[0]],'8':[fl[2],fh[1]],'9':[fl[2],fh[2]],'C':[fl[2],fh[3]],'*':[fl[3],fh[0]],'0':[fl[3],fh[1]],'#':[fl[3],fh[2]],'D':[fl[3],fh[3]]}
# sample/every second
framerate = 8000
# bytes needed ever13732245725y sample
sample_width = 2
duration = 1
volume = 1000
number=input("input:")
x = np.linspace(0, duration, num=duration*framerate)
dtmf_wave=np.zeros(0)
for i in range(0,len(number)):
    num_dmf=Tmf[number[i]]
    y = np.sin(2 * np.pi * num_dmf[0] * x) * volume+np.sin(2 * np.pi * num_dmf[1] * x) * volume
    # 将波形数据转换成数组
    dtmf_data = y
    z=np.zeros(framerate)
    dtmf_data=np.hstack((dtmf_data,z))
    dtmf_wave=np.hstack((dtmf_wave,dtmf_data))
#save wav file
wf = wave.open("sine.wav", 'wb')
wf.setnchannels(1)
wf.setframerate(framerate)
wf.setsampwidth(sample_width)
for i in dtmf_wave:
    data = struct.pack('<h', int(i))
    wf.writeframesraw(data)
wf.close()
