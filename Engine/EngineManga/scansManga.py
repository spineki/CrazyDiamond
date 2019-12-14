from Engine.EngineManga.engineMangas import EngineMangas
import json
import traceback
import time
import os
from tqdm import tqdm
"""
This class is in progress
"""

class EngineScansMangas(EngineMangas):
    """
    A class that parse, search and download manga from the website https://scans-mangas.com/mangas/
    """

    def __init__(self):
        super().__init__()
        self.reactive_keyword = ["scans-mangas"]
        self.break_time = 0.1
        self.name = "ScansManga"
        self.current_folder = os.path.dirname(__file__)
        self.list_manga_path = os.path.join(self.current_folder, "scans_mangas_list_manga.json")
        self.url_search  = "https://scans-mangas.com/mangas/"

    def get_list_volume_from_manga_url(self, url):
        """
        get the list of all volumes from a manga url

        ARGS:
            url -> string: url of the manga
        RETURN:
            dict with keys:
                "title" -> string : title of the manga
                ""chapter_list" -> dict with keys:
                    "link" -> string: link of the url of the chapter
                    "title" -> string: title of the chapter
                    "num" -> float or int: number of the chapter
        """

        def is_float(string):
            try:
                float(string)
                return True
            except ValueError:
                return False
        def is_int(float):
            try:
                int(float)
                return True
            except ValueError:
                return False

        soup = self.get_soup(url) # we get the soup related to the url
        results = soup.find_all("option", {"rel":"bookmark"})
        result_list = []
        for page in results:
            title = page.text.strip()
            list_number = [float(s) for s in title.split() if is_float(s)] # we need to handle decimal valued chapters
            list_number = [int(s) if  is_int(s) else s for s in list_number ]
            result_list.append({"link" : page["value"], "title": title, "num": list_number[-1]})
        result_list = sorted(result_list, key = lambda i: i['num'])
        title = soup.find("h1").text
        title = title.strip()
        return {"title" : title, "chapter_list" : result_list}

    def handle_chapter(self, url):
        """take the url of a chapter, return the manga_title, the chapter_num, the max number page, the pages dict {link, number}"""
        try:
            soup = self.get_soup(url)
            list_pages_found = soup.find_all("img", {"class": "lozad lazyload"})
            pages = []
            if list_pages_found == []:
                self.print_v("error, nothing found in the page" + url+ "I will try another time")
                url += "?view"
                soup = self.get_soup(url)
                list_pages_found = soup.find_all("img", {"class": "lozad lazyload"})
                pages = []
                if list_pages_found == []:
                    self.print_v("error, nothing found in the page another time" )
                    return False
                self.print_v("finally found " + url )

            for page in list_pages_found:
                name = page["alt"]
                indice = name.find("Page")
                num = int(name[indice+len("Page"):])
                pages.append({"link": page["data-src"], "num": num})

            first_page = list_pages_found[0]
            name = first_page["alt"]
            indice = name.find("Chapter")
            chapter_num = int(name[indice + len("chapter"):].strip().split()[0])
            manga_title = name.split(":")[0].strip()

            max_page = pages[-1]["num"]
            print(max_page, " found")
            return {"manga_title": manga_title, "chapter_num": chapter_num, "max_pages": max_page, "pages" : pages}
        except Exception as ex:
            self.print_v(str(ex))
            return False

    def download_chapter(self, url, directory=""):

        """ Retrieve all images from the manga chapter page, rename them and download them to the folder
                ARGS:
                    url:str: url of the given chapter: example "https://www.lelscan-vf.com/manga/the-promised-neverland/132"
                    directory
                RETURN:

                """
        results_chapter_page = self.handle_chapter(url)
        if results_chapter_page == False:
            return False
        directory = self.make_directory(directory)
        if directory == False:
            return False
        pages = results_chapter_page["pages"]
        chapter_num = results_chapter_page["chapter_num"]
        max_pages = results_chapter_page["max_pages"]
        manga_title = results_chapter_page["manga_title"]

        for page in pages:
            link = page["link"]
            number = page["num"]

            extension = link.rsplit(".")[-1].strip()
            save_name = self.purify_name(
                directory + manga_title + "_" + str(chapter_num) + "_" + str(number) + "." + extension)
            # here, we finally download the picture
            print(save_name, " the file we want to download")
            self.safe_download_picture(link, save_name)
            time.sleep(self.break_time)

    def download_manga(self, url, selection = "*", directory = ""):
            results_presentation_page = self.get_list_volume_from_manga_url(url)
            chapters = results_presentation_page["chapter_list"]
            self.print_v(str(len(chapters)) + " chapters found")
            if selection != "*":
                self.print_v("default selection range")
                chapters = [chapters[i] for i in range(int(selection[0])-1, int(selection[1])  )]

            root_directory = directory
            pbar = tqdm(chapters)
            i =  0
            maxi = len(chapters)

            for chapter in pbar:
                self.callback(int(i*10000/maxi)/100)
                i+=1
                folder_name = results_presentation_page["title"] + "_V" + str(chapter["num"])
                if root_directory == "":

                    directory = self.purify_name(os.path.join(self.dl_directory, results_presentation_page["title"] + "/" + folder_name + "/"))
                else:
                    directory = self.purify_name(os.path.join(root_directory, results_presentation_page["title"] + "/" + folder_name + "/"))
                self.print_v("Download in " + directory + "\n")
                pbar.set_description(chapter["title"] + " :")

                self.download_chapter(chapter["link"], directory)

    def get_all_available_manga_list(self):
        """
        return the list of all mangas available on the scansmanga website
        ARGS:
            None
        RETURN:

        EXAMPLE:
            RETURN:
            a list of dict with keys:
                "title": string -> name of the manga
                "link" : string -> url of the manga main page
            an empty list if no manga corresponds to the the name searched
        """

        results = []
        print('trying to get ' + self.url_search+ "in get_manga_search_page_list")
        soup = self.get_soup(self.url_search)

        list_mangas_found = soup.find_all("div", {"class": "item red"})
        for manga in list_mangas_found:
            results.append({"title": manga.find("h2").text, "link": manga.find("a")["href"]})
        return results

    def find_manga_by_name(self, name = ""):
        """ Search a 'manga' by its name in the database. If not found, make a requests, update the config, and search it again
            It returns every manga that has the name field in it's title
        Args:
            name (string): name of the required manga

        Returns:
            result (list): 'title' and links
                avec retour à la ligne\n
                test
            test (string): name of the manga.

            link (string): url of the manga main page.
            an empty list if no manga correspond to the the name searched

        Examples:
            find_manga_by_name("jojo"):
                * [{'title': 'JoJo’s Bizarre Adventure', 'link': 'https://scans-mangas.com/lecture-en-ligne/jojos-bizarre-adventure/'}]

            find_manga_by_name("naru"): [{'title': 'Ane Naru Mono', 'link': 'https://scans-mangas.com/lecture-en-ligne/ane-naru-mono/'},
                {'title': 'Curry Naru Shokutaku', 'link': 'https://scans-mangas.com/lecture-en-ligne/curry-naru-shokutaku/'},
                {'title': 'Naruto', 'link': 'https://scans-mangas.com/lecture-en-ligne/naruto/'},
                {'title': 'Yoru Ni Naru To Boku Wa', 'link': 'https://scans-mangas.com/lecture-en-ligne/yoru-ni-naru-to-boku-wa/'}]
         """


        results = [] # list of found manga
        found = False

        # first, we search the name in the database
        try:
            list_manga = self.get_json_file(self.list_manga_path)
        except:
            list_manga = []

        for manga in list_manga:
            if name.lower() in manga["title"].lower():
                found = True
                results.append(manga)

        # if the manga is not in the database, we look for it online
        if not found:
            self.print_v("search online " + name)
            # update the list
            list_manga = self.get_all_available_manga_list()
            # save the list in the file
            self.save_json_file(list_manga, self.list_manga_path)
            for manga in list_manga:
                if name.lower() in manga["title"].lower():
                    results.append(manga)
        return results

    def switch(self, search_word, selection ="*", directory = ""):
        self.log = []
        if "https" not in search_word: # we are looking for a title of a manga

            list_manga = self.find_manga_by_name(search_word)
            if list_manga != []:  # we found a corresponding manga
                self.print_v("Manga found in the database: " +  str(list_manga))
                chosen_manga = list_manga[0]
                url = chosen_manga["link"]
                self.download_manga(url, selection, directory)

        elif "uploads" in search_word: # we are looking for a single page
            items = search_word.rsplit(4)
            num_page = int(items[-1].split(".")[0])
            num_chapter = items[-2]
            title = items[-4]
            if directory =="":
                directory = self.purify_name(self.dl_directory + title + "/")
            self.make_directory(directory)
            save_name = self.purify_name(os.path.join(directory,  num_chapter + "_" + str(num_page) + "." + search_word.split(".")[-1]))

            self.download_picture(search_word, save_name)

        elif "lecture-en-ligne" in search_word: # we are lookin for a volume and all of its chapters
            self.download_manga(search_word, directory)

        else: # we are looking for a single chapter
            self.download_chapter(search_word, directory)
