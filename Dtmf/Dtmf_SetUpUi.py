# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dtmf1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(439, 238)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Lbtitle = QtWidgets.QLabel(self.centralwidget)
        self.Lbtitle.setGeometry(QtCore.QRect(20, 50, 72, 15))
        self.Lbtitle.setObjectName("Lbtitle")
        self.BthProduce = QtWidgets.QPushButton(self.centralwidget)
        self.BthProduce.setGeometry(QtCore.QRect(240, 40, 111, 31))
        self.BthProduce.setObjectName("BthProduce")
        self.BtnProcess = QtWidgets.QPushButton(self.centralwidget)
        self.BtnProcess.setGeometry(QtCore.QRect(260, 90, 160, 28))
        self.BtnProcess.setObjectName("BtnProcess")
        self.Lbtitle1 = QtWidgets.QLabel(self.centralwidget)
        self.Lbtitle1.setGeometry(QtCore.QRect(20, 150, 101, 16))
        self.Lbtitle1.setObjectName("Lbtitle1")
        self.Lbnumber = QtWidgets.QLabel(self.centralwidget)
        self.Lbnumber.setGeometry(QtCore.QRect(130, 150, 161, 20))
        self.Lbnumber.setObjectName("Lbnumber")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(100, 40, 131, 31))
        self.textEdit.setObjectName("textEdit")
        self.Bthclear = QtWidgets.QPushButton(self.centralwidget)
        self.Bthclear.setGeometry(QtCore.QRect(310, 140, 93, 28))
        self.Bthclear.setObjectName("Bthclear")
        self.LbPath = QtWidgets.QLabel(self.centralwidget)
        self.LbPath.setGeometry(QtCore.QRect(20, 100, 141, 16))
        self.LbPath.setObjectName("LbPath")
        self.BtnOpenFile = QtWidgets.QPushButton(self.centralwidget)
        self.BtnOpenFile.setGeometry(QtCore.QRect(180, 90, 41, 31))
        self.BtnOpenFile.setObjectName("BtnOpenFile")
        self.LbGroup = QtWidgets.QLabel(self.centralwidget)
        self.LbGroup.setGeometry(QtCore.QRect(20, 180, 151, 16))
        self.LbGroup.setObjectName("LbGroup")
        self.BtnPlay = QtWidgets.QPushButton(self.centralwidget)
        self.BtnPlay.setGeometry(QtCore.QRect(370, 40, 51, 31))
        self.BtnPlay.setObjectName("BtnPlay")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Bthclear.clicked.connect(self.Lbnumber.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DTMF"))
        self.Lbtitle.setText(_translate("MainWindow", "输入数字:"))
        self.BthProduce.setText(_translate("MainWindow", "生成音频文件"))
        self.BtnProcess.setText(_translate("MainWindow", "识别音频文字"))
        self.Lbtitle1.setText(_translate("MainWindow", "识别后的数字:"))
        self.Lbnumber.setText(_translate("MainWindow", "例:123456"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "输入想生成的数字"))
        self.Bthclear.setText(_translate("MainWindow", "清除"))
        self.LbPath.setText(_translate("MainWindow", "文件路径"))
        self.BtnOpenFile.setText(_translate("MainWindow", "..."))
        self.LbGroup.setText(_translate("MainWindow", "组员:张英杰，徐宇扬"))
        self.BtnPlay.setText(_translate("MainWindow", "播放"))
