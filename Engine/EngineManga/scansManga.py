from Engine.EngineManga.engineMangas import EngineMangas
import time
import os

class EngineScansMangas(EngineMangas):
    """
    A class that parses, searches and downloads mangas from the website https://scans-mangas.com/mangas/
    """

    def __init__(self):
        super().__init__()
        self.reactive_keyword = ["scans-mangas"]
        self.break_time = 0.1
        self.name = "ScansManga"
        self.current_folder = os.path.dirname(__file__)
        self.list_manga_path = os.path.join(self.current_folder, "scans_mangas_list_manga.json")
        self.url_search = "https://scans-mangas.com/mangas/"

    # INFO  ---------------------------------------------------------------------------------------
    def get_all_available_manga_list(self):
        """ Returns the list of all mangas available on the scansmanga website (after an online search)

        Args:
            None (None): None

        Returns:
            results (list): list of all found manga. Each element is a dict with the following keys
            {
            title (string): Name of the manga
            link (string): url of th emanga main page
            }
            None (None): None if there is no manga or an error

        Raises:
            Doesn't raise an error. print_v() errors.

        EXAMPLE:
            Wip
        """

        results = []

        soup = self.get_soup(self.url_search)
        if soup is None:
            return None
        try:
            list_mangas_found = soup.find_all("div", {"class": "item red"})
            for manga in list_mangas_found:
                results.append({"title": manga.find("h2").text, "link": manga.find("a")["href"]})
        except Exception as e:
            self.print_v("Impossible to find mangas in the page. Maybe tags are broken in ", self.url_search, ": ", str(e))

        if results == []:
            return None
        return results

    def find_manga_by_name(self, name):
        """ Searches a 'manga' by its name in the database. If not found, makes a requests, updates the config, and searches it again
            It returns every manga that has the name field in its title.
        Args:
            name (string): name of the required manga

        Returns:
            results (list): A list of dict with the following keys
            {
            title (string): Name of the manga
            link (string): url of th emanga main page
            }

            None if no manga corresponds to the the name searched

        Examples:
            >>> self.find_manga_by_name("jojo")
            >>> ouput: [{'title': 'JoJo’s Bizarre Adventure', 'link': 'https://scans-mangas.com/lecture-en-ligne/jojos-bizarre-adventure/'}]

            >>> self.find_manga_by_name("naru")
            >>> output: [{'title': 'Ane Naru Mono', 'link': 'https://scans-mangas.com/lecture-en-ligne/ane-naru-mono/'}, {'title': 'Curry Naru Shokutaku', 'link': 'https://scans-mangas.com/lecture-en-ligne/curry-naru-shokutaku/'}, {'title': 'Naruto', 'link': 'https://scans-mangas.com/lecture-en-ligne/naruto/'}, {'title': 'Yoru Ni Naru To Boku Wa', 'link': 'https://scans-mangas.com/lecture-en-ligne/yoru-ni-naru-to-boku-wa/'}]
         """

        # list of found manga
        results = []
        found = False

        # first, we search the name in the database
        list_manga = self.get_json_file(self.list_manga_path)
        if list_manga == None:
            list_manga = []

        for manga in list_manga:
            if name.lower() in manga["title"].lower():
                found = True
                results.append(manga)

        # If the manga is not in the database, we look for it online
        if not found:
            self.print_v("searching online " + name)
            # update the list
            list_manga = self.get_all_available_manga_list()
            if list_manga == None:
                return None

            # save the list in the file
            self.save_json_file(list_manga, self.list_manga_path)
            for manga in list_manga:
                if name.lower() in manga["title"].lower():
                    results.append(manga)

        if results == []:
            return None
        return results

    def get_list_volume_from_manga_url(self, url):
        """
        Gets the list of all volumes from a manga url

        Args:
            url (string): url of the manga

        Returns:
             A dict with the following keys
             {
            title (string): Title of the manga
            chapter_list (dict): A dictionnary with the following keys
            {
            link (string): link of the url of the chapter
            title (string): title of the chapter
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

        # We get the soup related to the url
        soup = self.get_soup(url)
        if soup is None:
            return None

        # We look for a specific tag in the page
        try:
            results = soup.find_all("option", {"rel": "bookmark"})
        except Exception as e:
            self.print_v("impossible to fin the 'option' tag in the webpage from ", url, ": ", str(e))
            return None

        # we extract titles, number of the volume....
        try:
            result_list = []
            for page in results:
                title = page.text.strip()
                # We need to handle decimal valued chapters
                list_number = [float(s) for s in title.split() if is_float(s)]
                list_number = [int(s) if is_int(s) else s for s in list_number]
                result_list.append({"link": page["value"], "title": title, "num": list_number[-1]})
        except Exception as e:
            self.print_v("Impossible to get proper numbers from the html page ", url, ": ", str(e))
            return None

        result_list = sorted(result_list, key=lambda i: i['num'])

        # We need the correct title as mentionned in the page
        try:
            title = soup.find("h1").text
            title = title.strip()

        except Exception as e:
            self.print_v("impossible to find the 'h1' tag for title in th page ", url, ": ", str(e))
            return None

        return {"title": title, "chapter_list": result_list}

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
            pages (list): a list of dictionnary with the following keys
            {
            link (string): link of the picture
            num (int): number of the picture (page)
            }
            }
            None (None): None if there is an error
        Raises:
            Doesn't raise an error. print a warning with self.print_v().

        Examples:
            Todo
        """

        soup = self.get_soup(url)
        if soup is None:
            return None

        # We extract all img fields.
        try:
            list_pages_found = soup.find_all("img", {"class": "lozad lazyload"})
        except Exception as e:
            self.print_v("Impossible to get the 'img' tag in the page ", url, ": ", str(e))
            return None

        # We try with a little hack to get the ?view page avoiding the adds
        if list_pages_found == []:
            self.print_v("error, nothing found in the page", url + " . I will try another time")
            url += "?view"
            soup = self.get_soup(url)
            if soup is None:
                return None
            try:
                list_pages_found = soup.find_all("img", {"class": "lozad lazyload"})
            except Exception as e:
                self.print_v("Impossible to get the 'img' tag in the page ", url, ": ", str(e))
                return None

            if list_pages_found == []:
                self.print_v("error, nothing found in the page even adding ?view")
                return None

        # We create the list of pages that are linked to this chapter
        pages = []
        try:
            for page in list_pages_found:
                name = page["alt"]
                index = name.find("Page")
                num = int(name[index + len("Page"):])
                pages.append({"link": page["data-src"], "num": num})
        except Exception as e:
            self.print_v("Impossible to get the 'alt' or 'Page' or 'link' tag in the page ", url, ": ", str(e))
            return None

        # We get general manga info as name, number of the chapter, manga_title, number max of pages
        first_page = list_pages_found[0]
        try:
            name = first_page["alt"]
            index = name.find("Chapter")
            chapter_num = int(name[index + len("chapter"):].strip().split()[0])
            manga_title = name.split(":")[0].strip()
            max_page = int(pages[-1]["num"])

        except Exception as e:
            self.print_v("Impossible to get tags 'alt' or 'Chapter'", ": ", str(e))
            return None

        return {"manga_title": manga_title, "chapter_num": chapter_num, "max_pages": max_page, "pages": pages}

    # DOWNLOAD ------------------------------------------------------------------------------------
    def download_chapter(self, url, folder_path= None):
        """ Download all images from the manga chapter page, rename them (purification) and download them
        ARGS:
            url (str): url of the given chapter.
            folder_path (string): default, default dl path. Path of the folder where images are downloaded.

        Returns:
            bool (bool): True if no error, False else

        Raises:
             Doesn't raise an error.

        Examples:
            wip
        """

        if folder_path is None:
            folder_path = self.dl_directory

        # We retrieve info from the chapter
        results_chapter_page = self.get_info_from_chapter_url(url)
        if results_chapter_page is None:
            return False

        # We create the download directory
        create_directory = self.make_directory(folder_path)
        if create_directory is False:
            return False

        # Unpacking values
        pages = results_chapter_page["pages"]
        chapter_num = results_chapter_page["chapter_num"]
        # max_pages = results_chapter_page["max_pages"]
        manga_title = results_chapter_page["manga_title"]

        for page in pages:
            link = page["link"]
            number = page["num"]
            extension = link.rsplit(".")[-1].strip()

            file_name = manga_title + "_" + str(chapter_num) + "_" + str(number) + "." + extension
            file_name = self.purify_name(file_name)
            save_name = os.path.join(folder_path, file_name)

            # here, we finally download the picture
            self.safe_download_picture(link, save_name)
            time.sleep(self.break_time)

        return True

    def async_download_chapter(self, url, folder_path=None):
        """ Download all images from the manga chapter page, rename them (purification) and download them
        ARGS:
            url (str): url of the given chapter.
            folder_path (string): default, default dl path. Path of the folder where images are downloaded.

        Returns:
            bool (bool): True if no error, False else

        Raises:
             Doesn't raise an error.

        Examples:
            wip
        """

        if folder_path is None:
            folder_path = self.dl_directory

        # We retrieve info from the chapter
        results_chapter_page = self.get_info_from_chapter_url(url)
        if results_chapter_page is None:
            return False

        # We create the download directory
        create_directory = self.make_directory(folder_path)
        if create_directory is False:
            return False

        # Unpacking values
        pages = results_chapter_page["pages"]
        chapter_num = results_chapter_page["chapter_num"]
        # max_pages = results_chapter_page["max_pages"]
        manga_title = results_chapter_page["manga_title"]

        url_list = []
        save_path_file_list = []
        for page in pages:
            link = page["link"]
            number = page["num"]
            extension = link.rsplit(".")[-1].strip()

            file_name = manga_title + "_" + str(chapter_num) + "_" + str(number) + "." + extension
            file_name = self.purify_name(file_name)
            save_name = os.path.join(folder_path, file_name)

            # here, we finally download the picture

            url_list.append(link)
            save_path_file_list.append(save_name)

        time.sleep(self.break_time)

        results = self.async_download_pictures(url_list, save_path_file_list)
        for elem in results:
            if elem == False:
                return False
        return True

    def download_manga(self, url, folder_path=None, async_mode = False):
        """ Download all images from the manga main page, rename them (purification) and download them
        ARGS:
            url (str): url of the given manga.
            selection (list): list of manga that will be downloaded
            folder_path (string): default, default dl path. Path of the folder where images are downloaded.

        Returns:
            bool (bool): True if no error, False else

        Raises:
            Doesn't raise an error.

        Examples:
            wip
        """
        # We gather main manga page info
        results_presentation_page = self.get_list_volume_from_manga_url(url)
        if results_presentation_page is None:
            return False

        chapters = results_presentation_page["chapter_list"]

        for chapter in chapters:

            folder_name = results_presentation_page["title"] + "_V" + str(chapter["num"])
            if folder_path is None:
                folder_path = self.dl_directory
            manga_directory = os.path.join(folder_path, results_presentation_page["title"])
            volume_directory = os.path.join(manga_directory, folder_name)
            volume_directory = self.purify_name(volume_directory)

            if async_mode:
                self.async_download_chapter(chapter["link"], volume_directory)
            else:
                self.download_chapter(chapter["link"], volume_directory)

        return True

    def download_volume_from_manga_name(self, name, number, folder_path = None, display_only = True):
        """
        Download a single volume just with the name of a manga
        Args:
            name (string): name of the manga
            number (string): number of the volume to be downloaded (maybe rename it to volume)
            folder_path (string): where to save the chapter. Default, dl

        Returns:
            bool (bool): False if the manga cannot be downloaded, list of bool if the donwload pass th esaync part

        Raises:
            None, but print_v() problems.

        """

        manga_list = self.find_manga_by_name(name)
        if manga_list is None:
            return False
        first_manga = manga_list[0]
        self.print_v(str(first_manga))

        results = self.get_list_volume_from_manga_url(first_manga["link"])

        if results is None:
            return False

        volume_list = results["chapter_list"]
        if volume_list == []:
            return False

        found = False
        found_volume = None
        for volume in volume_list:
            if volume["num"] == number:
                found = True
                found_volume = volume

        if not found:
            return False

        print(found_volume)

        if display_only:
            return True
        results = self.async_download_chapter(found_volume["link"])

        return results



    # SWITCH --------------------------------------------------------------------------------------
    def switch(self, search_word, selection ="*", directory = ""):
        """
        Work in progress, we need to rebuild this part.
        """

        # self.log = []
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
