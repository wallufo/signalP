from PyQt5 import QtCore, QtGui, QtWidgets
from ui_mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
import wave as we
import pygame
import numpy as np
import struct
import scipy as sc
import math
import matplotlib.pyplot as plt
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.BtnOpenFile.clicked.connect(self.openfile)
        self.BtnPlay.clicked.connect(self.playaudio)
        self.BthProduce.clicked.connect(self.produceAudio)
        self.BtnProcess.clicked.connect(self.processAudio)
    def openfile(self):
        Path,Type = QFileDialog.getOpenFileName(self,'选择文件','',"*.wav;;All Files(*)")
        if Path=="":
            QMessageBox.critical(self, "错误提示框", "没有选择任何文件！", QMessageBox.Yes | QMessageBox.No)
        else:
            print(Path)
            self.LbPath.setText(Path)
    def playaudio(self):
        path=self.LbPath.text()
        print(path)
        if path == "路径 例:E:\...":
            QMessageBox.critical(self, "错误提示框", "没有选择任何音频！", QMessageBox.Yes | QMessageBox.No)
        else:
            pygame.mixer.init()
            pygame.mixer.music.load(path) 
            pygame.mixer.music.set_volume(3) 
            pygame.mixer.music.play()
    def produceAudio(self):
        number=self.textEdit.toPlainText()
        print(number)
        fl=[697,770,852,941] #低频频率
        fh=[1209,1336,1477,1633] #高频频率
        Tmf={'1':[fl[0],fh[0]],'2':[fl[0],fh[1]],'3':[fl[0],fh[2]],'A':[fl[0],fh[3]],'4':[fl[1],fh[0]],'5':[fl[1],fh[1]],'6':[fl[1],fh[2]],'B':[fl[1],fh[3]],'7':[fl[2],fh[0]],'8':[fl[2],fh[1]],'9':[fl[2],fh[2]],'C':[fl[2],fh[3]],'*':[fl[3],fh[0]],'0':[fl[3],fh[1]],'#':[fl[3],fh[2]],'D':[fl[3],fh[3]]}
        # sample/every second
        framerate = 8000
        # bytes needed ever13732245725y sample
        sample_width = 2
        duration = 1
        volume = 1000
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
        DirPath = './Dtmf/sine.wav'
        wf = we.open(DirPath, 'wb')
        wf.setnchannels(1)
        wf.setframerate(framerate)
        wf.setsampwidth(sample_width)
        for i in dtmf_wave:
            data = struct.pack('<h', int(i))
            wf.writeframesraw(data)
        wf.close()
    def processAudio(self):
        def goertzel(simple,freq_indices,N):
            w = []
            c = []
            p = []
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
        Path=self.LbPath.text()
        f=we.open(Path,'rb')
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        strData = f.readframes(nframes)#读取音频，字符串格式
        waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int
        waveData = waveData*1.0/(max(abs(waveData)))#wave幅值归一化
        f.close()
        time = np.arange(0,nframes)*(1.0 / framerate)
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
        dtmf_number=[]
        num_dtmf=self.textEdit.toPlainText()
        print(num_dtmf)
        for fi in f:
            freq_indices.append(int(fi/fs*N))
        for i in range(0,datalength):
            if j>=len(num_dtmf):
                break
            if np.abs(waveData[k])>limit :
                x1=waveData[k:k+N]
                xk=goertzel(x1,freq_indices,N)
                num.append(findIndex(xk[0:3]))
                num.append(findIndex(xk[4:7]))
                print(tm[num[j*2],num[j*2+1]])
                dtmf_number.append(tm[num[j*2],num[j*2+1]])
                k=k+N
                j=j+1
            else:
                k=k+1
        num_str="".join([str(x) for x in dtmf_number])
        print(num_str)
        self.Lbnumber.setText(num_str)
        plt.plot(time,waveData)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Single channel wavedata")
        plt.show()
    