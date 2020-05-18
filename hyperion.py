import sys
from typing import List, Optional

from PySide2.QtGui import QColor

from Engine.EngineManga.manga import Volume, Manga, Chapter
from core import Core
from PySide2.QtWidgets import *
from gui.myWindow import Ui_MainWindow



# import engines: better create a proper core class and deal with it outside
from Engine.EngineManga.scanOP import EngineScanOP
# from Engine.EngineManga.mangaFox import EngineMangaFox
from Engine.EngineManga.lelScan import EngineLelscan
from Engine.EngineManga.scansManga import EngineScansMangas


class resultWidget(QListWidgetItem):
    """
    class for the line where result of search are displayed
    """
    def __init__(self, text: str, engine_name: str, manga: Manga):
        super().__init__(text)
        self.engine_name = engine_name
        self.manga = manga

class volumeWidget(QListWidgetItem):
    """
    class of lines where volume found are displayed
    """
    def __init__(self, text: str, volume: Volume):
        super().__init__(text)
        self.volume = volume

class chapterWidget(QListWidgetItem):
    """
    class of lines where volume found are displayed
    """
    def __init__(self, text: str, chapter: Chapter):
        super().__init__(text)
        self.chapter = chapter

class itemQueueWidget(QListWidgetItem):
    def __init__(self, manga_name, engine_name, number_string, subtext):
        self.text = "Vol. " + number_string +  "--\""+manga_name + "\""+ " from " + engine_name
        self.subtext= subtext
        super().__init__(self.text + " \n" + subtext)

    def modifyText(self, text):
        self.text = text
        self.setText(self.text + " \n" + self.subtext)

    def modifySubtext(self, subText):
        self.subtext = subText
        self.setText(self.text + " \n" + self.subtext)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.currentManga: Optional[Manga] = None
        self.currentVolume: Optional[Volume] = None
        self.currentChapter: Optional[Chapter] = None
        self.setupUi(self)
        self.startCore()
        self.setupEngines()
        self.assignWidgets()
        self.startingState()
        self.show()

    def startCore(self):
        self.core = Core()

    def assignWidgets(self):
        self.pushButton_analyse_auto.clicked.connect(self.auto_analyze)
        self.lineEdit_search.returnPressed.connect(self.auto_analyze)

        self.checkBox_range.stateChanged.connect(self.activateRange)
        self.checkBox_compress.stateChanged.connect(self.activateCompress)
        self.spinBox_volume.valueChanged.connect(self.namingVolume)
        self.pushButton_download.clicked.connect(self.download_selection)
        self.pushButton_download_all.clicked.connect(self.download_all)

    def auto_analyze(self):
        print("auto analyse")
        self.listWidget_results.clear()
        search_content = self.lineEdit_search.text()

        results = {}
        for e in self.engines:
            matching_mangas = e.find_manga_by_name(search_content)
            if matching_mangas is None: # no manga corresponding to this name
                continue

            # we store separately for each engine all the matching mangas
            results[e.name] = matching_mangas

        for engine_name in results:
            for matching_manga in results[engine_name]:
                item = resultWidget(text=matching_manga.name + " (à l'adresse) " +  matching_manga.link,
                                    engine_name=engine_name,
                                    manga=matching_manga)
                self.listWidget_results.addItem(item)

        self.listWidget_results.currentItemChanged.connect(self.fill_volume_chapters)
        self.label_nb_website_available.setText(str(self.listWidget_results.count()))

    def fill_volume_chapters(self):
        current_item: resultWidget = self.listWidget_results.currentItem()
        self.currentEngine = current_item.engine_name
        current_manga = current_item.manga

        self.lineEdit_url.setText(current_manga.link)
        self.lineEdit_manga_name.setText(current_manga.name)

        retrieved_manga: Optional[Manga] = self.get_engine_by_name(current_item.engine_name)\
            .get_list_volume_from_manga_url(current_manga.link)

        self.currentManga=retrieved_manga # we copy globally this manga, wich contains chapters, volume, etc

        volumes_list: List[Volume] = retrieved_manga.volumes_list
        chapters_without_volume_list: List[Chapter] = retrieved_manga.chapters_without_volumes_list

        self.label_nb_website_available.setText(str(len(volumes_list)))

        self.listWidget_volumes.clear()
        for volume in volumes_list:
            item = volumeWidget(text=str(volume.link) + ": " +  volume.name,
                                volume=volume)
            self.listWidget_volumes.addItem(item)
        self.listWidget_volumes.currentItemChanged.connect(self.volume_to_fields)

        self.listWidget_chapters.clear()
        for chapter in chapters_without_volume_list:
            item = chapterWidget(text=str(chapter.number) + " : " + chapter.name, chapter=chapter)
            self.listWidget_chapters.addItem(item)
        self.listWidget_chapters.currentItemChanged.connect(self.chapter_to_fields)

    def chapter_to_fields(self):
        print("chapter to fields")
        current_item: chapterWidget = self.listWidget_chapters.currentItem()
        current_chapter: Chapter = current_item.chapter
        self.currentChapter = current_chapter
        self.spinBox_volume.setValue(int(current_chapter.number))
        self.namingVolume()

    def volume_to_fields(self):
        print("volume to fields")
        current_item: volumeWidget = self.listWidget_volumes.currentItem()
        current_volume: Volume = current_item.volume
        self.currentVolume = current_volume

        self.spinBox_volume.setValue(int(current_volume.number))
        self.namingVolume()

    def fillQueue(self, manga_name, engine_name, number_string, subtext = "waiting..."):

        item = itemQueueWidget(manga_name, engine_name, number_string, subtext)
        self.listWidget_queue.addItem(item)

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
        # self.engines = [EngineScanOP(), EngineScansMangas(), EngineLelscan()] # EngineMangaFox()
        self.engines = [EngineScanOP()]

    def startingState(self):
        self.activateRange()
        self.activateCompress()

    def set_output_consol(self, text):
        self.label_console.setText(text)

    def get_engine_by_name(self, name):
        for e in self.engines:
            if e.name == name:
                return e
        return None

    def download_selection(self):
        print("download selection")
        manga_name = self.lineEdit_manga_name.text()
        manga_url = self.lineEdit_url.text()
        current_number = self.spinBox_volume.value()
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
            # graphical
            self.fillQueue(manga_name, engine.name, str(first_chap) + "_"+ str(last_chap))
            self.core.add_new_Task(function = engine.download_range_chapters_from_url,
                                   args = (manga_url, first_chap, last_chap, output_name),
                                   kwargs = {"compress": compress_ext},
                                   startCallback=self.startCallback,
                                   callback=self.callback,
                                   endCallback=self.endCallback)
        else:
            # normal mode, only for a single chapter
            #graphical
            self.fillQueue(manga_name, engine.name, str(current_number))
            self.core.add_new_Task(function=engine.download_range_chapters_from_url,
                                   args = (manga_url, current_number, current_number, output_name),
                                   kwargs = {"compress": compress_ext},
                                   startCallback=self.startCallback,
                                   callback=self.callback,
                                   endCallback=self.endCallback)

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

        self.fillQueue(manga_name, engine.name, str("all!"))
        self.core.add_new_Task(function=engine.download_whole_manga_from_url,
                               args=(manga_url, first_chap, last_chap, output_name),
                               kwargs={"async": compress_ext},
                               startCallback=self.startCallback,
                               callback=self.callback,
                               endCallback=self.endCallback)


        manga_url = self.lineEdit_url.text()
        engine.download_whole_manga_from_url(manga_url, async_mode=True)


    def startCallback(self, args = None, kwargs={}):
        self.listWidget_queue.item(0).modifySubtext("downloading!")
        self.listWidget_queue.item(0).setBackgroundColor(QColor(119,181,254))
        self.set_output_consol("Download of " + self.listWidget_queue.item(0).text)

    def callback(self, args=None, kwargs={}):
        pass

    def endCallback(self, args=None, kwargs={}):
        if args is None:
            self.set_output_consol("An error occured")
        elif args == False:
            self.set_output_consol("Your volume is not on the website\n try another one or some pictures are missing\n Verify in the download folder")
        else:
            self.set_output_consol("Download finished")
        self.listWidget_queue.takeItem(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)