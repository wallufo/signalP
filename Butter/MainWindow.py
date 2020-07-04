import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from butterui import Ui_MainWindow
from matplotlib.figure import Figure
import numpy as np
import sys
from PyQt5.QtWidgets import QMessageBox
from scipy.signal import butter, lfilter,buttord,freqs  
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.BtnOriginal.clicked.connect(self.paintOriginal)
        self.BtnButter.clicked.connect(self.paintButter)
        self.BtnProcess.clicked.connect(self.paintProcess)
    def paintOriginal(self):
        fs = 8000
        T = 10
        t = np.linspace(0, T, T*fs, endpoint=False)
        y = 5*np.sin(2*np.pi*t*500)+10*np.sin(2*np.pi*t*2500)
        f = np.linspace(0, fs, T*fs, endpoint=False) 
        ff = np.fft.fft(y)
        ff = np.abs(ff)*2/T/fs
        plt.figure()
        plt.plot(f, ff) 
        plt.show()
    def paintButter(self):
        fs=8000
        fstop=self.textFstop.toPlainText()
        fpass=self.textFpass.toPlainText()
        Astop=self.textAstop.toPlainText()
        Apass=self.textApass.toPlainText()
        if fstop=='' or fpass=='' or Astop=='' or Apass=='':
            QMessageBox.critical(self, "错误提示框", "参数错误！", QMessageBox.Yes | QMessageBox.No)
        else:
            fpass=int(fpass)
            fstop=int(fstop)
            Apass=int(Apass)
            Astop=int(Astop)
            N, Wn = buttord(np.pi*2*fpass, np.pi*2*fstop, Apass,Astop ,True) 
            wn=2*fstop/fs 
            b, a = butter(N,Wn,'low',analog=True)
            print(b,a)
            print(Wn)
            w,h=freqs(b,a)
            self.labelN.setText(str(N))
            self.labelWn.setText(str(wn))
            plt.figure()
            plt.semilogx(w/(2*np.pi), abs(h)/max(abs(h)))
            plt.show()
    def paintProcess(self):
        fs=8000
        N=self.labelN.text()
        wn=self.labelWn.text()
        N=int(N)
        wn=float(wn)
        T = 10
        t = np.linspace(0, T, T*fs, endpoint=False)
        y = 5*np.sin(2*np.pi*t*500)+10*np.sin(2*np.pi*t*2500)
        b, a = butter(N,wn, btype='lowpass')
        filterY = lfilter(b, a, y)
        ff = np.fft.fft(filterY)
        ff = np.abs(ff)*2/T/fs
        f = np.linspace(0, fs, T*fs, endpoint=False)
        plt.figure()
        plt.plot(f, ff)
        plt.show()
        
        