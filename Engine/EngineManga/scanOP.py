from Engine.EngineManga.engineMangas import EngineMangas
import os
import json
import sys
from Engine.EngineManga.manga import Manga, Volume, Chapter, Page
from typing import List, Optional


class EngineScanOP(EngineMangas):
    """
    A class that parses, searches and downloads mangas from the website https://scans-mangas.com/mangas/
    """

    def __init__(self):
        super().__init__()
        self.reactive_keyword = ["scan-op"]
        self.break_time = 0.1
        self.name = "Scan-OP"
        if getattr(sys, 'frozen', False):
            self.print_v("frozen mode")
            self.current_folder = os.path.dirname(sys.executable)
        else:
            self.current_folder = os.path.dirname(os.path.abspath(__file__))
        self.list_manga_path = os.path.join(self.current_folder, "scans_op_list_manga.json")
        self.url_search = "https://scan-op.com/search"
        self.url_manga = "https://scan-op.com/manga/"
        self.url_picture = "http://funquizzes.fun/uploads/manga/"

    # INFO  ---------------------------------------------------------------------------------------
    def get_all_available_manga_list(self) -> Optional[List[Manga]]:
        """Returns the list of all mangas available on the lelscan website (after an online search)

        Args:
            None (None): None

        Returns:
            results (list): list of all found manga. (Manga object)
            None (None): None if there is no manga or an error

        Raises:
            Doesn't raise an error. print_v() errors.

        Examples:
            TODO
        """

        soup = self.get_soup(self.url_search)
        if soup is None:
            return None

        saving_mangas_list = []

        try:
            archived_mangas_list = json.loads(soup.find("p").text)["suggestions"]

            for archived_manga in archived_mangas_list:
                saving_manga = Manga()

                name = archived_manga["value"]
                manga_identifier = archived_manga["data"]
                url = self.url_manga + manga_identifier

                saving_manga.name = name
                saving_manga.link = url

                saving_mangas_list.append(saving_manga)

        except Exception as e:
            self.print_v("Impossible to get the info from the ", self.url_search, " page. Maybe the site tags have change: ", str(e))
            return None

        return saving_mangas_list

    def get_list_volume_from_manga_url(self, url: str) -> Optional[Manga]:
        """
        a manga object

        Args:
            url (string): url of the manga

        Returns:
            list of volumes (list of object Volume)
            None (None): None if there is an error
        """
        def is_float(string):
            try:
                float(string)
                return True
            except ValueError:
                return False

        def is_int(_float):
            try:
                int(_float)
                return True
            except ValueError:
                return False

        soup = self.get_soup(url)
        if soup is None:
            return None

        retrieved_chapters_list = []
        try:
            name = soup.find("h2", {"class": "widget-title"}).text.strip()
            synopsis = soup.find("div", {"class": "well"}).find("p").text

            raw_chapters_list = soup.find_all("h5", {"class": "chapter-title-rtl"})
            for raw_chapter in raw_chapters_list:
                retrieved_chapter = Chapter(name=raw_chapter.find("em").text,
                                            link=raw_chapter.find("a")["href"])

                number_raw_chaper = raw_chapter.find("a").text
                list_number = [float(s) for s in number_raw_chaper.split() if is_float(s)]
                list_number = [int(s) if is_int(s) else s for s in list_number]
                retrieved_chapter.number = list_number[-1]

                retrieved_chapters_list.append(retrieved_chapter)

        except Exception as e:
            self.print_v("Impossible to get the correct tags from the soup from the page ", url, ": ", str(e))
            return None

        # there is no volume/chapter separation on scan op, so fill a default volume with number -1 with chapters
        # retrieved_volume = Volume()
        # retrieved_volume.add_chapters(retrieved_chapters_list)

        retrieved_manga = Manga(name=name, link=url, synopsis=synopsis)
        retrieved_manga.add_chapters_without_volume(retrieved_chapters_list)

        return retrieved_manga

    def get_info_from_chapter_url(self, url: str) -> Optional[Chapter]:
        """Takes the url of a chapter, and returns a set of valuable infos
            Args:
                url (string): url of the chapter
            Returns:
                chapter (Chapter): chapters
                None (None): None if there is an error
            Raises:
                Doesn't raise an error. print a warning with self.print_v().

            Examples:
                >>> e = EngineLelscan()
                >>> e.get_info_from_chapter_url("https://www.lelscan-vf.com/manga/shingeki-no-kyojin/22")
                >>> output: {'manga_title': 'Shingeki No Kyojin', 'chapter_num': '22', 'max_pages': 44, 'pages': [{'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/001.jpg ', 'num': 1}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/002.jpg ', 'num': 2}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/003.jpg ', 'num': 3}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/004.jpg ', 'num': 4}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/005.jpg ', 'num': 5}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/006.jpg ', 'num': 6}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/007.jpg ', 'num': 7}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/008.jpg ', 'num': 8}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/009.jpg ', 'num': 9}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/010.jpg ', 'num': 10}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/011.jpg ', 'num': 11}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/012.jpg ', 'num': 12}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/013.jpg ', 'num': 13}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/014.jpg ', 'num': 14}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/015.jpg ', 'num': 15}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/016.jpg ', 'num': 16}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/017.jpg ', 'num': 17}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/018.jpg ', 'num': 18}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/019.jpg ', 'num': 19}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/020.jpg ', 'num': 20}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/021.jpg ', 'num': 21}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/022.jpg ', 'num': 22}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/023.jpg ', 'num': 23}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/024.jpg ', 'num': 24}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/025.jpg ', 'num': 25}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/026.jpg ', 'num': 26}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/027.jpg ', 'num': 27}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/028.jpg ', 'num': 28}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/029.jpg ', 'num': 29}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/030.jpg ', 'num': 30}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/031.jpg ', 'num': 31}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/032.jpg ', 'num': 32}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/033.jpg ', 'num': 33}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/034.jpg ', 'num': 34}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/035.jpg ', 'num': 35}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/036.jpg ', 'num': 36}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/037.jpg ', 'num': 37}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/038.jpg ', 'num': 38}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/039.jpg ', 'num': 39}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/040.jpg ', 'num': 40}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/041.jpg ', 'num': 41}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/042.jpg ', 'num': 42}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/043.jpg ', 'num': 43}, {'link': ' https://www.lelscan-vf.com/uploads/manga/shingeki-no-kyojin/chapters/0022/044.jpg ', 'num': 44}]}
        """

        soup = self.get_soup(url)
        if soup is None:
            return None

        # if the chapter is missing, quits
        if not self.verify_missing_chapter(soup):
            return None

        try:  # Some blank pages can still pass
            manga_title = soup.find("img", {"class": "scan-page"})["alt"].split(":")[0].strip()
            list_number_page = [int(opt["value"]) for opt in soup.find_all("option") if "value" in opt.attrs]
            max_page = max(list_number_page)
        except Exception as e:
            self.print_v("Impossible to get 'img' and 'alt' fields in the soup from this url ", url, ": ", str(e))
            return None

        # Get the pictures links
        try:
            images_link = [img["data-src"] for img in soup.find_all("img", {"class": "img-responsive"}) if "data-src" in img.attrs]
        except Exception as e:
            self.print_v("Impossible to extract images link from the soup at the url ", url, ": ", str(e))
            return None

        if len(images_link) != len(list_number_page):
            self.print_v("Error, the number of pictures in the page doesn't match with the number of links, ", url, ": ")
            return None

        pages_list = []
        for i in range(len(images_link)):
            page = Page(number=list_number_page[i], link=images_link[i])
            pages_list.append(page)

        chapter_num = url.rsplit("/", 1)[-1]

        retrieved_chapter = Chapter()

        retrieved_chapter.manga_name = manga_title
        retrieved_chapter.number = chapter_num
        retrieved_chapter.number_page = max_page
        retrieved_chapter.add_pages(pages_list)

        return retrieved_chapter