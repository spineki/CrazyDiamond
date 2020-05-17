from Engine.EngineManga.engineMangas import EngineMangas
import json
import os
import sys
import requests
import bs4
import re



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

    def get_all_available_manga_list(self):

        """Returns the list of all mangas available on the lelscan website (after an online search)

        Args:
            None (None): None

        Returns:
            results (list): list of all found manga. Each element is a dict with the following keys
            {
            title (string): Name of the manga
            link (string): url of the manga main page
            }
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
        try:
            list_manga = []
            nb_pages = int(soup.find_all("a", {"class": "page-link"})[-1]["href"].split("/")[-2])

            for nbPage in range(1, nb_pages+1):
                page_url = self.url_search + str(nbPage)
                soup = self.get_soup(page_url, cookies=cookies)
                manga_field_in_page = soup.find_all("div", {"class": "manga-entry"})
                for manga_field in manga_field_in_page:
                    title_field = manga_field.find("a", {"class":"ml-1"})
                    title = title_field["title"]
                    link = self.url_manga +  title_field["href"]

                    list_manga.append({"title":title , "link":link})
        except Exception as e:
            self.print_v("Impossible to get the info from the ", self.url_search, " page. Maybe the site tags have change: ", str(e))
            return None


        return list_manga

    def get_list_volume_from_manga_url(self, url):
        """
        Gets the list of all volumes from a manga presentation page url

        Args:
            url (string): url of the manga

        Returns:
             A dict with the following keys
             {
            title (string): Title of the manga
            synopsis (string): synopsis of the manga
            chapter_list (dict): A dictionnary with the following keys
            {
            title (string): title of the chapter
            link (string): link of the url of the chapter
            num (float or int): number of the chapter
            }
            }
            None (None): None if there is an error
        """
        soup = self.get_soup(url)
        if soup is None:
            return None

        try:
            pattern = re.compile(r'Description')
            title = soup.find("span", {"class": "mx-1"}).text
            synopsis = (soup.find("div", {"class": "col-lg-3 col-xl-2 strong"}, text=pattern)) \
                .parent.find("div", {"class": "col-lg-9 col-xl-10"}).text
            max_chapter = int(soup.find("li", {"class":"page-item paging"}).find("a")["href"].split("/")[-2])

            chapter_list = []
            for nb_page in range(1, max_chapter+1):
                page_url = url + "/" + "chapters/" + str(nb_page)
                soup = self.get_soup(page_url)

                chapter_field_in_page = soup.find_all("a", {"class": "text-truncate"})
                for chapter_field in chapter_field_in_page:
                    text_field = chapter_field.text

                    elements = text_field.split("-")
                    chapter_title = elements[-1].strip()
                    chapter_link = self.url_manga + chapter_field["href"]
                    chapter_num = elements[0]


                    chapter_list.append({"title": chapter_title, "link": chapter_link, chapter_num})



        except Exception as e:
            self.print_v("Impossible to get the correct tags from the soup from the page ", url, ": ", str(e))
            return None




    def get_info_from_chapter_url(self, url):
        pass




if __name__ == '__main__':


    e = EngineMangadex()
    print(e.find_manga_by_name("shinge"))
