import sys
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from gui.myWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assignWidgets()
        self.show()

    def assignWidgets(self):
        self.pushButton_analyse_auto.clicked.connect(self.goPushed)
        self.pushButton_paste.clicked.connect(self.goPushed)

    def goPushed(self):
        print("youhou")
        self.lineEdit_search.setText("Go, Go, Go!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)