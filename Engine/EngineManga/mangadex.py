import os
import sys
import json
import requests
import bs4
from typing import List, Optional
import re

from Engine.EngineManga.engineMangas import EngineMangas
from Engine.EngineManga.manga import Manga, Volume, Chapter, Page

class EngineMangadex(EngineMangas):
    """
    A class that parses, searches and downloads mangas from the website https://www.lelscan-vf.com/
    """

    def __init__(self):

        super().__init__()
        self.reactive_keyword = ["mangadex"]
        self.break_time = 0.1
        self.name = "Mangadex"
        #self.current_folder = os.path.dirname(__file__)
        if getattr(sys, 'frozen', False):
            self.print_v("frozen mode")
            self.current_folder = os.path.dirname(sys.executable)
        else:
            self.current_folder = os.path.dirname(os.path.abspath(__file__))
        self.list_manga_path = os.path.join(self.current_folder, "mangadex_list_manga.json")
        # https://lelscan-vf.com/uploads/manga/dr-stone/chapters/125/01.png bellow
        self.url_picture = "https://lelscan-vf.com/uploads/manga/"
        # https://lelscan-vf.com/manga/tales-of-demons-and-gods bellow
        self.url_manga = "https://mangadex.org"
        self.url_search = "https://mangadex.org/titles/0/" # "https://mangadex.org/titles/0/1/"
        self.print_v(self.name + "created in " + self.current_folder)

    def get_all_available_manga_online_list(self)-> Optional[List[Manga]]:
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

        cookies = {"mangadex_title_mode": "2"}
        soup = self.get_soup(self.url_search, cookies=cookies) # cookie to create

        if soup is None:
            return None

        saving_mangas_list: List[Manga] = []
        try:
            nb_pages = int(soup.find_all("a", {"class": "page-link"})[-1]["href"].split("/")[-2])

            for nbPage in range(1, nb_pages+1):
                page_url = self.url_search + str(nbPage)
                soup = self.get_soup(page_url, cookies=cookies)
                manga_field_in_page = soup.find_all("div", {"class": "manga-entry"})
                for manga_field in manga_field_in_page:
                    title_field = manga_field.find("a", {"class":"ml-1"})
                    name = title_field["title"]
                    url = self.url_manga +  title_field["href"]

                    saving_manga = Manga()
                    saving_manga.name = name
                    saving_manga.link = url

                    saving_mangas_list.append(saving_manga)
        except Exception as e:
            self.print_v("Impossible to get the info from the ", self.url_search, " page. Maybe the site tags have change: ", str(e))
            return None

        return saving_mangas_list

    def get_manga_info_from_url(self, url) -> Optional[Manga]:
        """
        Gets the list of all volumes from a manga presentation page url

        Args:
            url (string): url of the manga

        Returns:
            manga filled with retrieved volumes and chapters
            None (None): None if there is an error
        """

        soup = self.get_soup(url)
        if soup is None:
            return None

        retrieved_chapters_list: List[Chapter] = []
        retrieved_volumes_list: List[Volume] = []
        retrieved_volumes_dict = {}
        try:
            pattern = re.compile(r'Description')
            manga_name = soup.find("span", {"class": "mx-1"}).text
            synopsis = (soup.find("div", {"class": "col-lg-3 col-xl-2 strong"}, text=pattern)) \
                .parent.find("div", {"class": "col-lg-9 col-xl-10"}).text
            max_chapter = int(soup.find("li", {"class":"page-item paging"}).find("a")["href"].split("/")[-2])


            for nb_page in range(1, max_chapter+1):
                page_url = url + "/" + "chapters/" + str(nb_page)
                soup = self.get_soup(page_url)

                chapter_field_in_page = soup.find_all("a", {"class": "text-truncate"})
                for chapter_field in chapter_field_in_page:

                    text_field = chapter_field.text
                    elements = text_field.split("-")

                    retrieved_chapter = Chapter(name=elements[-1].strip(),
                                                link=self.url_manga + chapter_field["href"])

                    raw_number = elements[0]

                    if "Vol." in raw_number:
                        string = raw_number.split("Vol.")[1].split("Ch. ")
                        volume_number = int(string[0].strip())
                        chapter_number = int(string[1].strip())
                    elif "Ch. " in raw_number:
                        volume_number = 0
                        chapter_number = int(raw_number.split("Ch. ")[1].strip())
                    else:
                        print(raw_number, " couldn't be parsed")
                        continue
                    retrieved_chapter.number = chapter_number

                    if volume_number not in retrieved_volumes_dict:
                        retrieved_volumes_dict[volume_number] = []
                    retrieved_volumes_dict[volume_number].append(retrieved_chapter)

        except Exception as e:
            self.print_v("Impossible to get the correct tags from the soup from the page ", url, ": ", str(e))
            return None


        # Now we put all the chapters in their volume
        for volume_number in retrieved_volumes_dict:
            if (volume_number == 0):
                for retrieved_chapter in retrieved_volumes_dict[0]:
                    retrieved_chapters_list.append(retrieved_chapter)
            else:
                retrieved_volume = Volume(number=volume_number)
                for chapter in retrieved_volumes_dict[volume_number]:
                    retrieved_volume.add_chapter(chapter)
                retrieved_volumes_list.append(retrieved_volume)




        retrieved_manga = Manga(name=manga_name, link=url, synopsis=synopsis)
        retrieved_manga.add_chapters_without_volume(retrieved_chapters_list)
        for retrieved_volume in retrieved_volumes_list:
            retrieved_manga.add_volume(retrieved_volume)

        return retrieved_manga

    def get_info_from_chapter_url(self, url) -> Optional[Chapter]:
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

        try:  # Some blank pages can still pass
            manga_title = soup.title.text.split("(")[1].split(")")[0]
            list_number_page = [int(opt["value"]) for opt in soup.find_all("option") if "value" in opt.attrs]
            max_page = max(list_number_page)
        except Exception as e:
            self.print_v("Impossible to get 'img' and 'alt' fields in the soup from this url ", url, ": ", str(e))
            return None



if __name__ == '__main__':


    e = EngineMangadex()
    print(e.find_manga_by_name("shinge"))
