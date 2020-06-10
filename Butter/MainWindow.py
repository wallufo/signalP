import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  
from PyQt5 import QtCore, QtGui, QtWidgets
from butterui import Ui_MainWindow
from matplotlib.figure import Figure
import numpy as np
import sys
from PyQt5.QtWidgets import QMessageBox
from scipy.signal import butter, lfilter,buttord,freqs  
class Figure_Canvas_Osignal(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键

    def __init__(self, parent=None, width=3, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)

        self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
    def originalSignal(self):
        fs = 8000
        T = 10
        t = np.linspace(0, T, T*fs, endpoint=False)
        y = 5*np.sin(2*np.pi*t*500)+10*np.sin(2*np.pi*t*2500)
        f = np.linspace(0, fs, T*fs, endpoint=False) 
        ff = np.fft.fft(y)
        ff = np.abs(ff)*2/T/fs
        self.axes.plot(f, ff) 
class Figure_Canvas_Bsignal(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键

    def __init__(self, parent=None, width=3, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)

        self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
    def butterSignal(self,w,h):
        self.axes.semilogx(w, 10 * np.log10(abs(h)))
class Figure_Canvas_Psignal(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键

    def __init__(self, parent=None, width=3, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure

        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)

        self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
    def processSignal(self,f,ff):
        self.axes.plot(f, ff)
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.BtnOriginal.clicked.connect(self.paintOriginal)
        self.BtnButter.clicked.connect(self.paintButter)
        self.BtnProcess.clicked.connect(self.paintProcess)
        self.graphicview = QtWidgets.QGraphicsView()  # 第一步，创建一个QGraphicsView
        self.graphicview.setObjectName("graphicview")      
    def paintOriginal(self):
        dr = Figure_Canvas_Osignal()
        #实例化一个FigureCanvas
        dr.originalSignal()  # 画图
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.GrapOriginal.setScene(graphicscene)       
        self.GrapOriginal.show()  # 最后，调用show方法呈现图形！Voila!!
    def paintButter(self):
        fs=8000
        fstop=self.textFstop.toPlainText()
        fpass=self.textFpass.toPlainText()
        Astop=self.textAstop.toPlainText()
        Apass=self.textApass.toPlainText()
        if fstop=='' or fpass=='' or Astop=='' or Apass=='':
            QMessageBox.critical(self, "错误提示框", "参数错误！", QMessageBox.Yes | QMessageBox.No)
        fpass=int(fpass)
        fstop=int(fstop)
        Apass=int(Apass)
        Astop=int(Astop)
        N, Wn = buttord(np.pi*2*fpass, np.pi*2*fstop, Apass,Astop ,True) 
        wn=2*fstop/fs 
        b, a = butter(N,wn,'high',analog=True)
        w,h=freqs(b,a,worN=np.logspace(-1, 2, 1000))
        self.labelN.setText(str(N))
        self.labelWn.setText(str(wn))
        dr1 = Figure_Canvas_Bsignal()
        #实例化一个FigureCanvas
        dr1.butterSignal(w,h)  # 画图
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(dr1)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.GrapButter.setScene(graphicscene)       
        self.GrapButter.show()  # 最后，调用show方法呈现图形！Voila!!
    def paintProcess(self):
        fs=8000
        N=self.labelN.text()
        wn=self.labelWn.text()
        N=int(N)
        wn=float(wn)
        T = 10
        t = np.linspace(0, T, T*fs, endpoint=False)
        y = 5*np.sin(2*np.pi*t*500)+10*np.sin(2*np.pi*t*2500)
        b, a = butter(N,wn, btype='highpass')
        filterY = lfilter(b, a, y)
        ff = np.fft.fft(filterY)
        ff = np.abs(ff)*2/T/fs
        f = np.linspace(0, fs, T*fs, endpoint=False)
        dr2 = Figure_Canvas_Psignal()
        #实例化一个FigureCanvas
        dr2.processSignal(f,ff)  # 画图
        graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        graphicscene.addWidget(dr2)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        self.GrapProcess.setScene(graphicscene)       
        self.GrapProcess.show()  # 最后，调用show方法呈现图形！Voila!! 
        