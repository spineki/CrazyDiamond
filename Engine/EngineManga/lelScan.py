from Engine.EngineManga.engineMangas import EngineMangas
import json
import time
import os
from tqdm import tqdm


class EngineLelscan(EngineMangas):

    def __init__(self):
        super().__init__()
        self.reactive_keyword = ["lelscan"]
        self.break_time = 0.1
        self.name = "EngineLelscan"
        self.current_folder = os.path.dirname(__file__)

        self.list_manga_path = os.path.join(self.current_folder, "lelscan_list_manga.json")
        self.url_picture = "https://lelscan-vf.com/uploads/manga/" # https://lelscan-vf.com/uploads/manga/dr-stone/chapters/125/01.png
        self.url_manga = "https://www.lelscan-vf.com/manga/"     # https://lelscan-vf.com/manga/tales-of-demons-and-gods
        self.url_search  = "https://lelscan-vf.com/search"

    def get_manga_search_page_list(self):
        """ retrieve list of all manga of the website"""
        soup = self.get_soup(self.url_search)
        list_manga = json.loads(soup.find("p").text)["suggestions"]
        return list_manga

    def search_manga(self, name):
        """ Search a manga in the database. If not, make a requests, update the config, and search it again"""
        results = []
        found = False
        print("recherche dans la base de donnee")
        try:
            list_manga = self.get_json_file(self.list_manga_path)
        except:
            list_manga = []
        for manga in list_manga:
            if name.lower() in manga["value"].lower():
                found = True
                results.append(manga)
        if not found:
            print("recherche en ligne")
            # update the list
            list_manga = self.get_manga_search_page_list()
            # save the list in the file
            self.save_json_file(list_manga, self.list_manga_path)
            for manga in list_manga:
                if name.lower() in manga["value"].lower():
                    results.append(manga)
        return results

    def handle_presentation_page(self, url):
        """ Find all chapter in the manga presentation page"""
        soup = self.get_soup(url)
        title = soup.find("h2", {"class": "widget-title"}).text.strip()
        synopsis = soup.find("div", {"class": "well"}).find("p").text
        chapter_list = [ {"title":chap.find("em").text, "chapter": chap.find("a").text, "link": chap.find("a")["href"]}   for chap in soup.find_all("h5", {"class": "chapter-title-rtl"})]
        return { "title":title, "synopsis":synopsis, "chapter_list":chapter_list}

    def handle_chapter(self, url):
        chapter_num = url.rsplit("/", 1)[-1]
        soup = self.get_soup(url)
        if not self.verify_missing_chapter(soup):
            print("un chapitre manquant", chapter_num)
            return False
        try: # some blank pages can still pass
            manga_title = soup.find("img", {"class": "scan-page"})["alt"].split(":")[0].strip()
            list_number_page = [int(opt["value"]) for opt in soup.find_all("option") if "value" in opt.attrs]
        except:
            return False
        max_page = max(list_number_page)

        images_link = [img["data-src"] for img in soup.find_all("img", {"class": "img-responsive"}) if
                       "data-src" in img.attrs]
        # print("max_pages"+ str(max_page)+ "image_links",  images_link)
        return {"manga_title":manga_title, "chapter_num": chapter_num, "max_pages": max_page, "image_links": images_link, "image_numbers":list_number_page}

    def download_chapter(self, url, directory = None):
        """ Retrieve all images from the manga chapter page, rename them and download them to the folder
        ARGS:
            url:str: url of the given chapter: example "https://www.lelscan-vf.com/manga/the-promised-neverland/132"
            directory
        RETURN:

        """

        results_chapter_page = self.handle_chapter(url)
        if results_chapter_page == False:
            return False


        image_links = results_chapter_page["image_links"]
        image_number = results_chapter_page["image_numbers"]
        chapter_num = results_chapter_page["chapter_num"]
        max_pages  = results_chapter_page["max_pages"]
        manga_title = results_chapter_page["manga_title"]
        if directory == None:
            directory = self.make_directory(os.path.join(self.dl_directory, self.purify_name(manga_title)))
        else:
            directory = self.make_directory(directory)
        for i in range(len(image_links)):
            link = image_links[i].strip()
            number = image_number[i]
            print("image ", i)
            extension = link.rsplit(".")[-1].strip()
            save_name = self.purify_name(os.path.join(directory , manga_title+"_"+ chapter_num + "_" + str(number) + "." + extension))

            print(save_name)
            # here, we finally download the picture
            self.download_picture(link, save_name)
            time.sleep(self.break_time)

    def download_manga(self, url, selection = "*", directory = ""):

            results_presentation_page = self.handle_presentation_page(url)
            chapters = results_presentation_page["chapter_list"]
            if directory == "":
                directory = self.purify_name(self.dl_directory + results_presentation_page["title"] + "/")
            else:
                directory = self.purify_name(directory + "/" + results_presentation_page["title"] + "/")
            self.print_v("debut du telechargement du manga dans " + directory)
            chapters.reverse() # we want the chapters in the good order
            self.print_v(str(len(chapters))+ " chapters found")
            if selection != "*":
                chapters = [chapters[i] for i in range(int(selection[0])-1, int(selection[1])  )]

            pbar = tqdm(chapters)
            i = 0
            maxi = len(chapters)
            for chapter in pbar:
                self.callback(int(i * 10000 / maxi) / 100)
                i+=1
                pbar.set_description(" :" + chapter["chapter"] + " | " + chapter["title"])
                # possibility to had a pbar
                # we get the page of single chapter
                self.download_chapter(chapter["link"], directory)

    def verify_missing_chapter(self, soup):
        """return False if a chapter is missing"""
        try:
            a = soup.find_all("div", {"class": "alert"})
            if a ==[]:
                return True
            a = a[0]
            if "Aucune page publiee" in a.text:
                return False
            return True
        except:
            self.print_v(soup.prettify())
            return False

    def switch(self, search_word, selection ="*", directory = ""):

        if "https" not in search_word: # we are looking for a title of a manga

            list_manga = self.search_manga(search_word)
            if list_manga != []:  # we found a corresponding manga
                print("Manga found: ",list_manga)
                chosen_manga = list_manga[0]

                url = self.url_manga + chosen_manga["data"]
                self.download_manga(url, selection, directory)

        elif "uploads" in search_word:
            items = search_word.rsplit(4)
            num_page = items[-1]
            num_chapter = items[-2]
            title = items[-4]
            if directory =="":
                directory = self.purify_name(self.dl_directory + title + "/")
            self.make_directory(directory)
            save_name = self.purify_name(directory + num_chapter + "_" + str(num_page) + "." + search_word.split(".")[-1])
            self.download_picture(search_word, save_name)

        elif "manga" in search_word:
            right_part_url = search_word.rsplit("/", 1)

            if right_part_url[-1].isdigit(): # thus, we are look to the home page of a chapter:
                self.download_chapter(search_word, directory)

            else: # thus, it's the main page of the manga, were we can look for chapters
                self.download_manga(search_word, directory)


