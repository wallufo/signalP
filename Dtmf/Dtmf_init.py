import sys
import Dtmf_SetUpUi as Dui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
if __name__ == "__main__":  
    app = QApplication(sys.argv) 
    widgets = QtWidgets.QMainWindow()
    ui = Dui.Ui_MainWindow()
    ui.setupUi(widgets)
    widgets.show()
    sys.exit(app.exec_())