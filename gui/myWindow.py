# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'myWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1183, 912)
        self.action_d = QAction(MainWindow)
        self.action_d.setObjectName(u"action_d")
        self.actionencore_un = QAction(MainWindow)
        self.actionencore_un.setObjectName(u"actionencore_un")
        self.actionyayaayay = QAction(MainWindow)
        self.actionyayaayay.setObjectName(u"actionyayaayay")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 30, 841, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_recherche = QLabel(self.horizontalLayoutWidget)
        self.label_recherche.setObjectName(u"label_recherche")

        self.horizontalLayout.addWidget(self.label_recherche)

        self.lineEdit_search = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_search.setObjectName(u"lineEdit_search")

        self.horizontalLayout.addWidget(self.lineEdit_search)

        self.pushButton_paste = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_paste.setObjectName(u"pushButton_paste")
        self.pushButton_paste.setStyleSheet(u"background-color: rgb(255, 0, 0);\n"
"color: rgb(255,255,255);")

        self.horizontalLayout.addWidget(self.pushButton_paste)

        self.progressBar_progress = QProgressBar(self.centralwidget)
        self.progressBar_progress.setObjectName(u"progressBar_progress")
        self.progressBar_progress.setGeometry(QRect(190, 720, 711, 31))
        self.progressBar_progress.setValue(0)
        self.pushButton_analyse_auto = QPushButton(self.centralwidget)
        self.pushButton_analyse_auto.setObjectName(u"pushButton_analyse_auto")
        self.pushButton_analyse_auto.setGeometry(QRect(420, 80, 141, 23))
        self.pushButton_analyse_auto.setStyleSheet(u"background-color: rgb(27, 126, 25);\n"
"color: rgb(255, 255, 255)")
        self.label_image = QLabel(self.centralwidget)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setGeometry(QRect(260, 490, 151, 51))
        self.label_image.setScaledContents(False)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(280, 130, 301, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(660, 300, 47, 13))
        self.gridLayoutWidget_2 = QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(280, 270, 431, 44))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_url = QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_url.setObjectName(u"lineEdit_url")

        self.gridLayout_2.addWidget(self.lineEdit_url, 1, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(280, 390, 431, 51))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1)

        self.spinBox_chap_start = QSpinBox(self.gridLayoutWidget)
        self.spinBox_chap_start.setObjectName(u"spinBox_chap_start")
        self.spinBox_chap_start.setMaximum(99999)
        self.spinBox_chap_start.setValue(1)

        self.gridLayout.addWidget(self.spinBox_chap_start, 1, 1, 1, 1)

        self.spinBox_chap_end = QSpinBox(self.gridLayoutWidget)
        self.spinBox_chap_end.setObjectName(u"spinBox_chap_end")
        self.spinBox_chap_end.setMaximum(99999)
        self.spinBox_chap_end.setValue(1)

        self.gridLayout.addWidget(self.spinBox_chap_end, 1, 3, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.checkBox_range = QCheckBox(self.gridLayoutWidget)
        self.checkBox_range.setObjectName(u"checkBox_range")

        self.gridLayout.addWidget(self.checkBox_range, 1, 0, 1, 1)

        self.gridLayoutWidget_3 = QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(280, 330, 431, 44))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.gridLayoutWidget_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.lineEdit_manga_name = QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_manga_name.setObjectName(u"lineEdit_manga_name")

        self.gridLayout_3.addWidget(self.lineEdit_manga_name, 1, 0, 1, 1)

        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(280, 550, 431, 41))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.lineEdit_save_path = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_save_path.setObjectName(u"lineEdit_save_path")

        self.verticalLayout.addWidget(self.lineEdit_save_path)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(280, 460, 331, 41))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.verticalLayoutWidget_2)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_2.addWidget(self.label_10)

        self.lineEdit_output_name = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_output_name.setObjectName(u"lineEdit_output_name")

        self.verticalLayout_2.addWidget(self.lineEdit_output_name)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(620, 460, 91, 41))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.verticalLayoutWidget_3)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.spinBox_volume = QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_volume.setObjectName(u"spinBox_volume")
        self.spinBox_volume.setMaximum(99999)
        self.spinBox_volume.setValue(1)

        self.verticalLayout_3.addWidget(self.spinBox_volume)

        self.checkBox_compress = QCheckBox(self.centralwidget)
        self.checkBox_compress.setObjectName(u"checkBox_compress")
        self.checkBox_compress.setGeometry(QRect(410, 600, 121, 17))
        self.comboBox_compress_mode = QComboBox(self.centralwidget)
        self.comboBox_compress_mode.addItem("")
        self.comboBox_compress_mode.addItem("")
        self.comboBox_compress_mode.setObjectName(u"comboBox_compress_mode")
        self.comboBox_compress_mode.setGeometry(QRect(500, 600, 69, 22))
        self.listWidget_results = QListWidget(self.centralwidget)
        self.listWidget_results.setObjectName(u"listWidget_results")
        self.listWidget_results.setGeometry(QRect(280, 160, 431, 91))
        self.pushButton_download = QPushButton(self.centralwidget)
        self.pushButton_download.setObjectName(u"pushButton_download")
        self.pushButton_download.setGeometry(QRect(380, 660, 211, 41))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(27, 126, 25, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(0, 170, 0, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush2)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush2)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush2)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush3 = QBrush(QColor(255, 255, 255, 128))
        brush3.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush3)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        brush4 = QBrush(QColor(255, 255, 255, 128))
        brush4.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush4)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        brush5 = QBrush(QColor(255, 255, 255, 128))
        brush5.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush5)
#endif
        self.pushButton_download.setPalette(palette)
        self.pushButton_download.setAutoFillBackground(False)
        self.pushButton_download.setStyleSheet(u"background-color: rgb(27, 126, 25);\n"
"color: rgb(255, 255, 255)")
        self.label_console = QLabel(self.centralwidget)
        self.label_console.setObjectName(u"label_console")
        self.label_console.setGeometry(QRect(40, 810, 1021, 61))
        self.label_console.setStyleSheet(u"background-color: rgb(0, 0, 0);\n"
"color:rgb(0, 255, 0)")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(40, 790, 151, 16))
        self.pushButton_download_all = QPushButton(self.centralwidget)
        self.pushButton_download_all.setObjectName(u"pushButton_download_all")
        self.pushButton_download_all.setGeometry(QRect(740, 430, 141, 23))
        self.pushButton_download_all.setStyleSheet(u"background-color: rgb(255, 0, 0);\n"
"color: rgb(255,255,255);")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(720, 330, 91, 41))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(810, 350, 3, 61))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(793, 460, 20, 111))
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(720, 570, 81, 16))
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.listWidget_volumes = QListWidget(self.centralwidget)
        self.listWidget_volumes.setObjectName(u"listWidget_volumes")
        self.listWidget_volumes.setGeometry(QRect(10, 160, 251, 431))
        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 130, 181, 21))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.horizontalLayoutWidget_2)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_2.addWidget(self.label_12)

        self.label_nb_vol_available = QLabel(self.horizontalLayoutWidget_2)
        self.label_nb_vol_available.setObjectName(u"label_nb_vol_available")

        self.horizontalLayout_2.addWidget(self.label_nb_vol_available)

        self.listWidget_queue = QListWidget(self.centralwidget)
        self.listWidget_queue.setObjectName(u"listWidget_queue")
        self.listWidget_queue.setGeometry(QRect(895, 161, 271, 431))
        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(900, 140, 47, 13))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1183, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.action_d)
        self.menu.addAction(self.actionencore_un)
        self.menu.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_d.setText(QCoreApplication.translate("MainWindow", u"aide", None))
        self.actionencore_un.setText(QCoreApplication.translate("MainWindow", u"param\u00e8tres", None))
        self.actionyayaayay.setText(QCoreApplication.translate("MainWindow", u"yayaayay", None))
        self.label_recherche.setText(QCoreApplication.translate("MainWindow", u"Nom du manga (pas forc\u00e9ment au complet)", None))
        self.pushButton_paste.setText(QCoreApplication.translate("MainWindow", u"coller: ne fonctione pas encore", None))
        self.pushButton_analyse_auto.setText(QCoreApplication.translate("MainWindow", u"Analyse automatique", None))
        self.label_image.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sites trouv\u00e9s:double-cliquez sur celui que vous voulez choisir", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Url du manga (automatique, mais vous pouvez le modifier)", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Chapitre de d\u00e9but(inclu)", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Chapitre de fin (inclu)", None))
        self.checkBox_range.setText(QCoreApplication.translate("MainWindow", u"Regrouper des chapitres \n"
"dans un m\u00eame volume", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Nom du manga (automatique, mais vous pouvez le modifier)", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Dossier d'enregistrement: par d\u00e9faut, dans le dossier dl d'Hyp\u00e9rion", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Nom du fichier de sortie (automatique, mais vous pouvez le modifier)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Num\u00e9ro du volume", None))
        self.checkBox_compress.setText(QCoreApplication.translate("MainWindow", u"Compresser?", None))
        self.comboBox_compress_mode.setItemText(0, QCoreApplication.translate("MainWindow", u".pdf", None))
        self.comboBox_compress_mode.setItemText(1, QCoreApplication.translate("MainWindow", u".cbz", None))

        self.pushButton_download.setText(QCoreApplication.translate("MainWindow", u"T\u00e9l\u00e9charger", None))
        self.label_console.setText(QCoreApplication.translate("MainWindow", u" Aucune erreur pour le moment", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Sortie console en cas d'erreur", None))
        self.pushButton_download_all.setText(QCoreApplication.translate("MainWindow", u"Je veux tout t\u00e9l\u00e9charger", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Nombre de volume/chapters dispo:", None))
        self.label_nb_vol_available.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Queue", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"menu", None))
    # retranslateUi

