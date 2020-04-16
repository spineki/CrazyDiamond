from Engine.EngineManga.engineMangas import EngineMangas
import json
import os


class EngineLelscan(EngineMangas):
    """
    A class that parses, searches and downloads mangas from the website https://www.lelscan-vf.com/
    """

    def __init__(self):
        super().__init__()
        self.reactive_keyword = ["lelscan"]
        self.break_time = 0.1
        self.name = "Lelscan"
        self.current_folder = os.path.dirname(__file__)
        self.list_manga_path = os.path.join(self.current_folder, "lelscan_list_manga.json")
        # https://lelscan-vf.com/uploads/manga/dr-stone/chapters/125/01.png bellow
        self.url_picture = "https://lelscan-vf.com/uploads/manga/"
        # https://lelscan-vf.com/manga/tales-of-demons-and-gods bellow
        self.url_manga = "https://www.lelscan-vf.com/manga/"
        self.url_search = "https://lelscan-vf.com/search"

    # INFO  ---------------------------------------------------------------------------------------
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

        soup = self.get_soup(self.url_search)
        if soup is None:
            return None

        try:
            list_manga = json.loads(soup.find("p").text)["suggestions"]

            for manga in list_manga:
                title = manga["value"]
                del manga["value"]
                manga["title"] = title
                manga_identifier = manga["data"]
                del manga["data"]
                manga["link"] = self.url_manga + manga_identifier

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
        try:
            title = soup.find("h2", {"class": "widget-title"}).text.strip()
            synopsis = soup.find("div", {"class": "well"}).find("p").text
            chapter_list = [ {"title":chap.find("em").text, "num": chap.find("a").text, "link": chap.find("a")["href"]}   for chap in soup.find_all("h5", {"class": "chapter-title-rtl"})]
            for chapter in chapter_list:
                list_number = [float(s) for s in chapter["num"].split() if is_float(s)]
                list_number = [int(s) if is_int(s) else s for s in list_number]
                chapter["num"] = list_number[-1]

        except Exception as e:
            self.print_v("Impossible to get the correct tags from the soup from the page ", url, ": ", str(e))
            return None

        return { "title":title, "synopsis":synopsis, "chapter_list":chapter_list}

    def get_info_from_chapter_url(self, url):
        """Takes the url of a chapter, and returns a set of valuable infos
            Args:
                url (string): url of the chapter
            Returns:
                Dictionnary with the following keys
                {
                manga_title (string): title of the manga
                chapter_num (int): number of the current chapter
                max_pages (int): number of pages in the current chapter
                pages (list): A list of dictionnary with the following keys
                {
                link (string): link of the picture
                num (int): number of the picture (page)
                }
                }
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

        try: # Some blank pages can still pass
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

        pages = []
        for i in range(len(images_link)):
            pages.append({"link": images_link[i], "num": list_number_page[i]})

        chapter_num = url.rsplit("/", 1)[-1]
        return {"manga_title": manga_title, "chapter_num": chapter_num, "max_pages": max_page, "pages": pages}

    # DOWNLOAD ------------------------------------------------------------------------------------
    def verify_missing_chapter(self, soup):
        """Verify if a chapter is missing
        Args:
            soup (soup): Beautiful soup object containing html code of the page

        Returns:
            bool (bool): True if the page is not empty, False else

        Raises:
            doesn't raise an error. print_v() warnings
        """
        try:
            # We search the alert tag that appears on empty pages
            a = soup.find_all("div", {"class": "alert"})
            if a ==[]:
                return True

            a = a[0]
            if "Aucune page publiee" in a.text:
                return False
            return True

        except Exception as e:
            self.print_v("impossible to properly parse the soup", soup.prettify(), str(e))
            return False

    # SWITCH --------------------------------------------------------------------------------------
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


