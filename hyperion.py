import sys
from typing import List, Optional

from PySide2.QtGui import QColor

from Engine.EngineManga.manga import Volume, Manga, Chapter
from core import Core
from PySide2.QtWidgets import *
from gui.myWindow import Ui_MainWindow


# import engines: better create a proper core class and deal with it outside
from Engine.engine import Engine
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
        self.text = "Vol. " + number_string + "--\"" + \
            manga_name + "\"" + " from " + engine_name
        self.subtext = subtext
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
        """
        Launch a core instance

        :return: None
        """
        self.core = Core()

    def assignWidgets(self):
        """
        connect widgets to their function

        :return: None
        """
        self.pushButton_analyse_auto.clicked.connect(self.auto_analyze)
        self.lineEdit_search.returnPressed.connect(self.auto_analyze)

        self.checkBox_range.stateChanged.connect(self.activateRange)
        self.checkBox_compress.stateChanged.connect(self.activateCompress)
        self.spinBox_volume.valueChanged.connect(self.namingVolume)
        self.pushButton_download.clicked.connect(self.download_selection)
        self.pushButton_download_volume.clicked.connect(self.download_volume)
        self.pushButton_download_all.clicked.connect(self.download_all)

    def auto_analyze(self):
        """
        analyse the name of the manga and search matching in every engine.

        :return: None
        """
        print("auto analyse")
        self.listWidget_results.clear()
        search_content = self.lineEdit_search.text()

        results = {}
        for e in self.engines:
            matching_mangas = e.find_manga_by_name(search_content)
            if matching_mangas is None:  # no manga corresponding to this name
                continue

            # we store separately for each engine all the matching mangas
            results[e.name] = matching_mangas

        for engine_name in results:
            for matching_manga in results[engine_name]:
                item = resultWidget(text=matching_manga.name + " (à l'adresse) " + matching_manga.link,
                                    engine_name=engine_name,
                                    manga=matching_manga)
                self.listWidget_results.addItem(item)

        self.listWidget_results.currentItemChanged.connect(
            self.fill_volume_chapters)
        self.label_nb_website_available.setText(
            str(self.listWidget_results.count()))

    def fill_volume_chapters(self):
        """
        Fill volumes and chapters from the clicked manga

        :return: None
        """
        current_item: resultWidget = self.listWidget_results.currentItem()
        self.currentEngine = current_item.engine_name
        current_manga = current_item.manga

        self.lineEdit_url.setText(current_manga.link)
        self.lineEdit_manga_name.setText(current_manga.name)

        retrieved_manga: Optional[Manga] = self.get_engine_by_name(current_item.engine_name)\
            .get_manga_info_from_url(current_manga.link)

        # we copy globally this manga, wich contains chapters, volume, etc
        self.currentManga = retrieved_manga

        volumes_list: List[Volume] = retrieved_manga.volumes_list
        chapters_without_volume_list: List[Chapter] = retrieved_manga.chapters_without_volumes_list

        self.label_nb_website_available.setText(str(len(volumes_list)))

        self.listWidget_volumes.clear()
        for volume in volumes_list:
            min_chap_number, max_chap_number = volume.get_min_max_number_chapters()
            item = volumeWidget(text=str(volume.number) + ": containing " + "chapters " + str(min_chap_number) + " - " + str(max_chap_number),
                                volume=volume)
            self.listWidget_volumes.addItem(item)
        self.listWidget_volumes.currentItemChanged.connect(
            self.volume_to_fields)
        self.label_nb_vol_available.setText(
            str(self.listWidget_volumes.count()))

        self.listWidget_chapters.clear()
        for chapter in chapters_without_volume_list:
            item = chapterWidget(text=str(chapter.number) +
                                 " : " + chapter.name, chapter=chapter)
            self.listWidget_chapters.addItem(item)
        self.listWidget_chapters.currentItemChanged.connect(
            self.chapter_to_fields)
        self.label_nb_chap_available.setText(
            str(self.listWidget_chapters.count()))

    def chapter_to_fields(self):
        """
        Copy clicked chapter info to the textEntry field

        :return: None
        """
        print("chapter to fields")
        current_item: chapterWidget = self.listWidget_chapters.currentItem()
        current_chapter: Chapter = current_item.chapter
        self.currentChapter = current_chapter
        self.spinBox_volume.setValue(int(current_chapter.number))
        self.namingVolume()

    def volume_to_fields(self):
        """
        Add chapters of a specific volume to the chapter field

        :return: None
        """

        current_item: volumeWidget = self.listWidget_volumes.currentItem()
        current_volume: Volume = current_item.volume
        self.currentVolume = current_volume

        self.listWidget_chapters.clear()
        for chapter in current_volume.chapters_list:
            item = chapterWidget(text=str(chapter.number) +
                                 " : " + chapter.name, chapter=chapter)
            self.listWidget_chapters.addItem(item)
        self.listWidget_chapters.currentItemChanged.connect(
            self.chapter_to_fields)
        self.label_nb_chap_available.setText(
            str(self.listWidget_chapters.count()))

        self.spinBox_volume.setValue(int(current_volume.number))
        self.namingVolume()

    def fillQueue(self, manga_name: str, engine_name: str, number_string: str, subtext="waiting...") -> None:
        """
        Add an itemQueueWidget to the queue

        :param str manga_name: Name of the manga
        :param str engine_name: Name of the engine to process the current manga
        :param str number_string: Volume or chapter number
        :param str subtext: subtext to give more information about the current download
        :return: None
        """
        item = itemQueueWidget(manga_name, engine_name, number_string, subtext)
        self.listWidget_queue.addItem(item)

    def namingVolume(self):
        """
        Automatically fill the output_name field thanks to the name and nuùber field
        :return:
        """
        name = self.lineEdit_manga_name.text()
        number = self.spinBox_volume.value()

        self.lineEdit_output_name.setText(name + "_V" + str(number))

    def activateRange(self):
        """
        Allow spinbox interaction (choose the chapter range) once the checkbox is checked
        :return: None
        """
        if self.checkBox_range.checkState():  # activate cross = true
            self.spinBox_chap_end.setEnabled(True)
            self.spinBox_chap_start.setEnabled(True)
        else:
            self.spinBox_chap_end.setEnabled(False)
            self.spinBox_chap_start.setEnabled(False)

    def activateCompress(self):
        """
        Allow combobox interaction once the checkbox "compress" is checked
        :return: None
        """
        if self.checkBox_compress.checkState():  # activate cross = true
            self.comboBox_compress_mode.setEnabled(True)
        else:
            self.comboBox_compress_mode.setEnabled(False)

    def setupEngines(self):
        """
        create an array of used engines

        :return: None
        """

        self.currentEngine = None
        self.engines = [EngineScanOP(), EngineScansMangas(),
                        EngineLelscan()]  # EngineMangaFox()

    def startingState(self):
        """
        set the init state (compression disabled, range disabled)

        :return: None
        """

        self.activateRange()
        self.activateCompress()

    def set_output_consol(self, text: str):
        """
        Print the given text to the output consol

        :param str text:
        :return: None
        """
        self.label_console.setText(text)

    def get_engine_by_name(self, name: str) -> Optional[Engine]:
        """
        Return the engine which contains the given name
        :param name:
        :return:
        """
        for e in self.engines:
            if e.name == name:
                return e
        return None

    def download_selection(self):
        """
        Download a chapter or a range of chapter according to the checked state of the gui

        :return: None
        """

        print("download selection")
        manga_name = self.lineEdit_manga_name.text()
        manga_url = self.lineEdit_url.text()
        folder_path = self.lineEdit_save_path.text()
        if folder_path == "":
            folder_path = None
        current_number = self.spinBox_volume.value()
        first_chap = self.spinBox_chap_start.value()
        last_chap = self.spinBox_chap_end.value()
        compress = self.checkBox_compress.checkState()
        if compress:
            compress_ext = self.comboBox_compress_mode.currentText()
        else:
            compress_ext = None
        output_name = self.lineEdit_output_name.text()

        if self.currentEngine is None:  # temporary
            print("pas de manga sélectionné")
            return

        engine = None
        for e in self.engines:
            if e.name == self.currentEngine:
                engine = e
                break

        if self.checkBox_range.checkState():  # if range of chapter mode
            # graphical
            self.fillQueue(manga_name, engine.name, str(
                first_chap) + "_" + str(last_chap))
            self.core.add_new_Task(function=engine.download_range_chapters_from_url,
                                   args=(manga_url, first_chap,
                                         last_chap, output_name),
                                   kwargs={"compress": compress_ext,
                                           "folder_path": folder_path},
                                   startCallback=self.startCallback,
                                   callback=self.callback,
                                   endCallback=self.endCallback)
        else:
            # normal mode, only for a single chapter
            # graphical
            self.fillQueue(manga_name, engine.name, str(current_number))
            self.core.add_new_Task(function=engine.download_range_chapters_from_url,
                                   args=(manga_url, current_number,
                                         current_number, output_name),
                                   kwargs={"compress": compress_ext,
                                           "folder_path": folder_path},
                                   startCallback=self.startCallback,
                                   callback=self.callback,
                                   endCallback=self.endCallback)

    def download_volume(self):
        """
        Download selected volume
        :return: None
        """

        manga_name = self.lineEdit_manga_name.text()
        compress = self.checkBox_compress.checkState()
        folder_path = self.lineEdit_save_path.text()
        if folder_path.strip() == "":
            folder_path = None

        if compress:
            compress_ext = self.comboBox_compress_mode.currentText()
        else:
            compress_ext = None
        output_name = self.lineEdit_output_name.text()

        if self.currentEngine is None:  # temporary
            print("pas de manga sélectionné")
            return

        engine = None
        for e in self.engines:
            if e.name == self.currentEngine:
                engine = e
                break

        volume = self.currentVolume
        manga = self.currentManga

        self.fillQueue(manga_name, engine.name, str(volume.number))
        self.core.add_new_Task(function=engine.download_volume_from_manga_url,
                               args=(manga.link, volume.number, folder_path),
                               kwargs={"compress": compress_ext,
                                       "display_only": False},
                               startCallback=self.startCallback,
                               callback=self.callback,
                               endCallback=self.endCallback)

    def download_all(self):
        """
        Download full selected manga

        :return: None
        """
        manga_name = self.lineEdit_manga_name.text()
        manga_url = self.lineEdit_url.text()
        compress = self.checkBox_compress.checkState()
        output_name = self.lineEdit_output_name.text()
        if compress:
            compress_ext = self.comboBox_compress_mode.currentText()
        else:
            compress_ext = None
        if self.currentEngine is None:  # temporary
            print("pas de manga sélectionné")
            return

        engine = None
        for e in self.engines:

            if e.name == self.currentEngine:
                engine = e
                break

        print("avant whole", compress_ext)
        self.fillQueue(manga_name, engine.name, str("all!"))
        self.core.add_new_Task(function=engine.download_whole_manga_from_url,
                               args=(manga_url),
                               kwargs={"compress": compress_ext},
                               startCallback=self.startCallback,
                               callback=self.callback,
                               endCallback=self.endCallback)

    def startCallback(self, args=None, kwargs={}):
        """
        A callback template that would be called before a download

        :param args: an array of args
        :param kwargs: a dict of kwargs
        :return: None
        """
        self.listWidget_queue.item(0).modifySubtext("downloading!")
        self.listWidget_queue.item(0).setBackgroundColor(QColor(119, 181, 254))
        self.set_output_consol(
            "Download of " + self.listWidget_queue.item(0).text)

    def callback(self, args=None, kwargs={}):
        pass

    def endCallback(self, args=None, kwargs={}):
        if args is None:
            self.set_output_consol("An error occured")
        elif args == False:
            self.set_output_consol(
                "Your volume is not on the website\n try another one or some pictures are missing\n Verify in the download folder")
        else:
            self.set_output_consol("Download finished")
        self.listWidget_queue.takeItem(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
