# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1103, 828)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 841, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_recherche = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_recherche.setObjectName("label_recherche")
        self.horizontalLayout.addWidget(self.label_recherche)
        self.lineEdit_search = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.pushButton_paste = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_paste.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"color: rgb(255,255,255);")
        self.pushButton_paste.setObjectName("pushButton_paste")
        self.horizontalLayout.addWidget(self.pushButton_paste)
        self.progressBar_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_progress.setGeometry(QtCore.QRect(170, 670, 711, 31))
        self.progressBar_progress.setProperty("value", 0)
        self.progressBar_progress.setObjectName("progressBar_progress")
        self.pushButton_analyse_auto = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_analyse_auto.setGeometry(QtCore.QRect(420, 80, 141, 23))
        self.pushButton_analyse_auto.setStyleSheet("background-color: rgb(27, 126, 25);\n"
"color: rgb(255, 255, 255)")
        self.pushButton_analyse_auto.setObjectName("pushButton_analyse_auto")
        self.label_image = QtWidgets.QLabel(self.centralwidget)
        self.label_image.setGeometry(QtCore.QRect(260, 490, 151, 51))
        self.label_image.setText("")
        self.label_image.setScaledContents(False)
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image.setObjectName("label_image")
        self.widget_queue = QtWidgets.QWidget(self.centralwidget)
        self.widget_queue.setGeometry(QtCore.QRect(900, 50, 191, 551))
        self.widget_queue.setObjectName("widget_queue")
        self.listView_results = QtWidgets.QListView(self.centralwidget)
        self.listView_results.setGeometry(QtCore.QRect(280, 160, 431, 81))
        self.listView_results.setObjectName("listView_results")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 130, 301, 16))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(660, 300, 47, 13))
        self.label_4.setObjectName("label_4")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(280, 270, 431, 44))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_url = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.gridLayout_2.addWidget(self.lineEdit_url, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(280, 390, 431, 51))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1)
        self.spinBox_chap_start = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_chap_start.setObjectName("spinBox_chap_start")
        self.gridLayout.addWidget(self.spinBox_chap_start, 1, 1, 1, 1)
        self.spinBox_chap_end = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_chap_end.setObjectName("spinBox_chap_end")
        self.gridLayout.addWidget(self.spinBox_chap_end, 1, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.checkBox_range = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox_range.setObjectName("checkBox_range")
        self.gridLayout.addWidget(self.checkBox_range, 1, 0, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(280, 330, 431, 44))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_manga_name = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_manga_name.setObjectName("lineEdit_manga_name")
        self.gridLayout_3.addWidget(self.lineEdit_manga_name, 1, 0, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(280, 550, 431, 41))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit_save_path = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_save_path.setObjectName("lineEdit_save_path")
        self.verticalLayout.addWidget(self.lineEdit_save_path)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(280, 460, 331, 41))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_2.addWidget(self.label_10)
        self.lineEdit_output_name = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_output_name.setObjectName("lineEdit_output_name")
        self.verticalLayout_2.addWidget(self.lineEdit_output_name)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(620, 460, 91, 41))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.spinBox_volume = QtWidgets.QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_volume.setObjectName("spinBox_volume")
        self.verticalLayout_3.addWidget(self.spinBox_volume)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(910, 30, 171, 20))
        self.label_11.setObjectName("label_11")
        self.checkBox_compress = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_compress.setGeometry(QtCore.QRect(330, 600, 121, 17))
        self.checkBox_compress.setObjectName("checkBox_compress")
        self.comboBox_compress_mode = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_compress_mode.setGeometry(QtCore.QRect(420, 600, 69, 22))
        self.comboBox_compress_mode.setObjectName("comboBox_compress_mode")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1103, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_d = QtWidgets.QAction(MainWindow)
        self.action_d.setObjectName("action_d")
        self.actionencore_un = QtWidgets.QAction(MainWindow)
        self.actionencore_un.setObjectName("actionencore_un")
        self.actionyayaayay = QtWidgets.QAction(MainWindow)
        self.actionyayaayay.setObjectName("actionyayaayay")
        self.menu.addAction(self.action_d)
        self.menu.addAction(self.actionencore_un)
        self.menu.addSeparator()
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_recherche.setText(_translate("MainWindow", "URL ou nom du manga: "))
        self.pushButton_paste.setText(_translate("MainWindow", "coller"))
        self.pushButton_analyse_auto.setText(_translate("MainWindow", "Analyse automatique"))
        self.label.setText(_translate("MainWindow", "Sites trouvés:double-cliquez sur celui que vous voulez choisir"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Url du manga (automatique, mais vous pouvez le modifier)"))
        self.label_9.setText(_translate("MainWindow", "Chapitre de début(inclu)"))
        self.label_8.setText(_translate("MainWindow", "Chapitre de fin (inclu)"))
        self.checkBox_range.setText(_translate("MainWindow", "Regrouper des chapitres \n"
"dans un même volume"))
        self.label_2.setText(_translate("MainWindow", "Nom du manga (automatique, mais vous pouvez le modifier)"))
        self.label_5.setText(_translate("MainWindow", "Dossier d\'enregistrement: par défaut, dans le dossier dl d\'Hypérion"))
        self.label_10.setText(_translate("MainWindow", "Nom du fichier de sortie (automatique, mais vous pouvez le modifier)"))
        self.label_7.setText(_translate("MainWindow", "Numéro du volume"))
        self.label_11.setText(_translate("MainWindow", "Queue: pas encore implémentée"))
        self.checkBox_compress.setText(_translate("MainWindow", "Compresser?"))
        self.menu.setTitle(_translate("MainWindow", "menu"))
        self.action_d.setText(_translate("MainWindow", "aide"))
        self.actionencore_un.setText(_translate("MainWindow", "paramètres"))
        self.actionyayaayay.setText(_translate("MainWindow", "yayaayay"))
