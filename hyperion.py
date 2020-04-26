import sys
from PySide2.QtWidgets import *
from gui.myWindow import Ui_MainWindow

# import engines: better create a proper core class and deal with it outside
from Engine.EngineManga.scanOP import EngineScanOP
# from Engine.EngineManga.mangaFox import EngineMangaFox
from Engine.EngineManga.lelScan import EngineLelscan
from Engine.EngineManga.scansManga import EngineScansMangas


class resultWidget(QListWidgetItem):

    def __init__(self, text, engine_name, link, manga_name):
        super().__init__(text)
        self.engine_name = engine_name
        self.manga_name = manga_name
        self.link= link

class volumeWidget(QListWidgetItem):
    def __init__(self, text, link, volume):
        super().__init__(text)
        self.link = link
        self.volume = volume


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setupEngines()
        self.assignWidgets()
        self.startingState()
        self.show()

    def assignWidgets(self):
        self.pushButton_analyse_auto.clicked.connect(self.auto_analyze)
        self.checkBox_range.stateChanged.connect(self.activateRange)
        self.checkBox_compress.stateChanged.connect(self.activateCompress)
        self.spinBox_volume.valueChanged.connect(self.namingVolume)
        self.pushButton_download.clicked.connect(self.download)
        self.pushButton_download_all.clicked.connect(self.download_all)

    def auto_analyze(self):
        self.listWidget_results.clear()
        search_content = self.lineEdit_search.text()

        results = {}
        for e in self.engines:
            r = e.find_manga_by_name(search_content)
            if r is None: # no manga corresponding to this name
                continue

            results[e.name] = r

        for engine_name in results:
            for info_manga in results[engine_name]:
                item = resultWidget(info_manga["title"] + " (à l'adresse) " +  info_manga["link"],
                                    engine_name,
                                    info_manga["link"],
                                    info_manga["title"])
                self.listWidget_results.addItem(item)

        self.listWidget_results.currentItemChanged.connect(self.autoFill)

    def autoFill(self):
        current_item = self.listWidget_results.currentItem()
        self.currentEngine = current_item.engine_name
        self.lineEdit_url.setText(current_item.link)
        self.lineEdit_manga_name.setText(current_item.manga_name)

        result = self.get_engine_by_name(current_item.engine_name).get_list_volume_from_manga_url(current_item.link)
        chapter_list=result["chapter_list"]
        self.label_nb_vol_available.setText(str(len(chapter_list)))

        self.listWidget_volumes.clear()
        for chapter in chapter_list:
            item = volumeWidget( str(chapter["num"]) + ": titre: " +  chapter["title"],
                                    chapter["link"],
                                    chapter["num"])
            self.listWidget_volumes.addItem(item)

        self.listWidget_volumes.currentItemChanged.connect(self.fillVolume)

    def fillVolume(self):
        current_item = self.listWidget_volumes.currentItem()
        self.spinBox_volume.setValue(int(current_item.volume))


        self.namingVolume()


    def namingVolume(self):
        name = self.lineEdit_manga_name.text()
        number = self.spinBox_volume.value()

        self.lineEdit_output_name.setText(name + "_V" + str(number))

    def activateRange(self):
        if self.checkBox_range.checkState(): # activate cross = true
            self.spinBox_chap_end.setEnabled(True)
            self.spinBox_chap_start.setEnabled(True)
        else:
            self.spinBox_chap_end.setEnabled(False)
            self.spinBox_chap_start.setEnabled(False)

    def activateCompress(self):
        if self.checkBox_compress.checkState(): # activate cross = true
            self.comboBox_compress_mode.setEnabled(True)
        else:
            self.comboBox_compress_mode.setEnabled(False)

    def setupEngines(self):
        self.currentEngine = None
        self.engines = [EngineScanOP(), EngineScansMangas(), EngineLelscan()] # EngineMangaFox()

    def startingState(self):
        self.activateRange()
        self.activateCompress()

    def set_output_consol(self, text):
        self.label_console.setText(text)

    def download_all(self):
        manga_name = self.lineEdit_manga_name.text()
        manga_url = self.lineEdit_url.text()
        volume_number = self.spinBox_volume.value()
        first_chap = self.spinBox_chap_start.value()
        last_chap = self.spinBox_chap_end.value()
        compress = self.checkBox_compress.checkState()
        output_name = self.lineEdit_output_name.text()

        if self.currentEngine is None: # temporary
            print("pas de manga sélectionné")
            return

        engine = None
        for e in self.engines:

            if e.name == self.currentEngine:
                engine = e
                break

        manga_url = self.lineEdit_url.text()
        engine.download_manga_from_url(manga_url, async_mode=True)

    def get_engine_by_name(self, name):
        for e in self.engines:
            if e.name == name:
                return e
        return None

    def download(self):

        manga_name = self.lineEdit_manga_name.text()
        manga_url = self.lineEdit_url.text()
        volume_number = self.spinBox_volume.value()
        first_chap = self.spinBox_chap_start.value()
        last_chap = self.spinBox_chap_end.value()
        compress = self.checkBox_compress.checkState()
        if compress:
            compress_ext = self.comboBox_compress_mode.currentText()
        else:
            compress_ext = None
        output_name = self.lineEdit_output_name.text()


        if self.currentEngine is None: # temporary
            print("pas de manga sélectionné")
            return

        engine = None
        for e in self.engines:
            if e.name == self.currentEngine:
                engine = e
                break

        if self.checkBox_range.checkState(): # if range of chapter mode
            print("range mode")
            result = engine.download_range_chapters_from_name(manga_name, first_chap, last_chap, output_name, compress = compress_ext)
            print(result)
        else:
            # normal mode, only for a single chapter
            print("single volume")
            result = engine.download_volume_from_manga_url(manga_url, volume_number, volume_name=output_name, display_only=False, compress = compress_ext)
            if result == False:
                self.set_output_consol("Your volume is not on the website\n try another one or some pictures are missing\n Verify in the download folder")
            elif result == None:
                self.set_output_consol("An error occured")
            else:
                self.set_output_consol("Download of " + manga_name + str(volume_number) + " finished")
            print(result)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)