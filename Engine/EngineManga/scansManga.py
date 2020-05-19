from Engine.EngineManga.engineMangas import EngineMangas
import os
import sys
from typing import List, Optional

from Engine.EngineManga.manga import Manga, Volume, Chapter, Page


class EngineScansMangas(EngineMangas):
    """
    A class that parses, searches and downloads mangas from the website https://scans-mangas.com/mangas/
    """

    def __init__(self):
        super().__init__()
        self.reactive_keyword = ["scans-mangas"]
        self.break_time = 0.1
        self.name = "ScansManga"
        # self.current_folder = os.path.dirname(__file__)
        if getattr(sys, 'frozen', False):
            self.print_v("frozen mode")
            self.current_folder = os.path.dirname(sys.executable)
        else:
            self.current_folder = os.path.dirname(os.path.abspath(__file__))
        self.list_manga_path = os.path.join(self.current_folder, "scans_mangas_list_manga.json")
        self.url_search = "https://scans-mangas.com/mangas/"
        self.url_root = "https://scans-mangas.com"
        self.print_v(self.name + "created in " + self.current_folder)

        # INFO  ---------------------------------------------------------------------------------------

    def get_all_available_manga_list(self)  -> Optional[List[Manga]]:
        """ Returns the list of all mangas available on the scansmanga website (after an online search)

        Args:

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
            return []

        saving_mangas_list: List[Manga] = []
        try:
            online_mangas_list = soup.find_all("div", {"class": "item red"})
            for online_manga in online_mangas_list:
                saving_manga = Manga()

                name = online_manga.find("h2").text
                url = online_manga.find("a")["href"]

                saving_manga.name = name
                saving_manga.link = url

                saving_mangas_list.append(saving_manga)

        except Exception as e:
            self.print_v("Impossible to find mangas in the page. Maybe tags are broken in ",
                         self.url_search, ": ", str(e))
            return None

        return saving_mangas_list

    def get_manga_info_from_url(self, url: str) -> Optional[Manga]:
        """
        Gets the list of all volumes from a manga url

        Args:
            url (string): url of the manga

        Returns:
            manga filled with retrieved volumes and chapters
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

        # We get the soup related to the url
        soup = self.get_soup(url)
        if soup is None:
            return None

        # We look for a specific tag in the page
        try:
            raw_page_list = soup.find_all("option", {"rel": "bookmark"})
        except Exception as e:
            self.print_v("impossible to fin the 'option' tag in the webpage from ", url, ": ", str(e))
            return None

        # we extract titles, number of the volume....
        retrieved_chapters_list: List[Chapter] = []
        try:
            for page in raw_page_list:
                retrieved_chapter = Chapter(name=page.text.strip(),
                                            link=page["value"])

                title = page.text.strip()
                # get rid of , converted to dot
                raw_title = title.replace(",", ".")

                # We need to handle decimal valued chapters
                list_number = [float(s) for s in raw_title.split() if is_float(s)]
                list_number = [int(s) if is_int(s) else s for s in list_number]
                retrieved_chapter.number = list_number[-1]

                retrieved_chapters_list.append(retrieved_chapter)

        except Exception as e:
            self.print_v("Impossible to get proper numbers from the html page ", url, ": ", str(e))
            return None

        retrieved_chapters_list = sorted(retrieved_chapters_list, key=lambda manga: manga.number)

        # We need the correct title as mentioned in the page
        try:
            name = soup.find("h1").text.strip()

        except Exception as e:
            self.print_v("impossible to find the 'h1' tag for title in th page ", url, ": ", str(e))
            return None

        retrieved_manga = Manga(name=name, link=url, synopsis="")  # TODO: get synopsis
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
         """

        soup = self.get_soup(url)
        if soup is None:
            return None

        # We extract all img fields.
        try:
            found_pages_list = soup.find_all("img", {"class": "lozad lazyload"})
        except Exception as e:
            self.print_v("Impossible to get the 'img' tag in the page ", url, ": ", str(e))
            return None

        # We try with a little hack to get the ?view page avoiding the adds
        if found_pages_list == []:
            self.print_v("error, nothing found in the page", url + " . I will try another time")
            url += "?view"
            soup = self.get_soup(url)
            if soup is None:
                return None
            try:
                found_pages_list = soup.find_all("img", {"class": "lozad lazyload"})
            except Exception as e:
                self.print_v("Impossible to get the 'img' tag in the page ", url, ": ", str(e))
                return None

            if found_pages_list == []:
                self.print_v("error, nothing found in the page even adding ?view")
                return None

        # We create the list of pages that are linked to this chapter
        pages_list: List[Page] = []
        try:
            for page in found_pages_list:
                name = page["alt"]
                index = name.find("Page")
                num = int(name[index + len("Page"):])
                if page["data-src"][:8] == "https://":
                    link = page["data-src"]
                else:
                    link = self.url_root + page["data-src"]

                retrieved_page = Page(number=num, link=link)

                pages_list.append(retrieved_page)

        except Exception as e:
            self.print_v("Impossible to get the 'alt' or 'Page' or 'link' tag in the page ", url, ": ", str(e))
            return None

        # We get general manga info as name, number of the chapter, manga_title, number max of pages
        first_page = found_pages_list[0]
        try:
            name = first_page["alt"]
            index = name.find("Chapter")
            chapter_num = int(name[index + len("chapter"):].strip().split()[0])
            manga_title = name.split(":")[0].strip()
            max_page = int(pages_list[-1].number)

        except Exception as e:
            self.print_v("Impossible to get tags 'alt' or 'Chapter'", ": ", str(e))
            return None

        retrieved_chapter = Chapter()
        retrieved_chapter.manga_name = manga_title
        retrieved_chapter.number = chapter_num
        retrieved_chapter.number_page = max_page
        retrieved_chapter.add_pages(pages_list)

        return retrieved_chapter
