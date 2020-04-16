import sys
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from gui.myWindow import Ui_MainWindow

# import engines: better create a proper core class and deal with it outside
from Engine.EngineManga.scanOP import EngineScanOP
from Engine.EngineManga.mangaFox import EngineMangaFox
from Engine.EngineManga.lelScan import EngineLelscan
from Engine.EngineManga.scansManga import EngineScansMangas


class resultWidget(QListWidgetItem):

    def __init__(self, text, engine_name, link, manga_name):
        super().__init__(text)
        self.engine_name = engine_name
        self.manga_name = manga_name
        self.link= link


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setupEngines()
        self.assignWidgets()
        self.show()

    def assignWidgets(self):
        self.pushButton_analyse_auto.clicked.connect(self.auto_analyze)
        self.pushButton_paste.clicked.connect(self.goPushed)

    def auto_analyze(self):
        search_content = self.lineEdit_search.text()

        results = {}
        for e in self.engines:
            r = e.find_manga_by_name(search_content)
            if r is None: # no manga corresponding to this name
                continue

            results[e.name] = r

        for engine_name in results:
            for info_manga in results[engine_name]:
                item = resultWidget(info_manga["title"] + " __à l'adresse__ " +  info_manga["link"],
                                    engine_name,
                                    info_manga["link"],
                                    info_manga["title"])
                # item = QListWidgetItem(info_manga["title"] + "|" +  info_manga["link"])
                self.listWidget_results.addItem(item)

        self.listWidget_results.currentItemChanged.connect(self.autoFill)


    def autoFill(self):
        current_item = self.listWidget_results.currentItem()
        self.lineEdit_url.setText(current_item.link)
        self.lineEdit_manga_name.setText(current_item.manga_name)
        print(current_item.link)
        # now we have a dictionnary

    def goPushed(self):
        print("youhou")
        self.lineEdit_search.setText("Go, Go, Go!")

    def setupEngines(self):
        self.engines = [EngineScanOP(), EngineScansMangas(), EngineLelscan()] # EngineMangaFox()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)