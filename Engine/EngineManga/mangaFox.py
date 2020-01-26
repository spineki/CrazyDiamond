from Engine.EngineManga.engineMangas import EngineMangas
import os


class EngineMangaFox(EngineMangas):
    """
    A class that parses, searches and downloads mangas from the website https://ww3.mangafox.online/
    """

    def __init__(self):
        super().__init__()
        self.reactive_keyword = ["scans-mangas"]
        self.break_time = 0.1
        self.name = "ScansManga"
        self.current_folder = os.path.dirname(__file__)
        self.list_manga_path = os.path.join(self.current_folder, "manag_fox_list_manga.json")
        self.url_search = "https://ww3.mangafox.online/alphabet/"

    # INFO  ---------------------------------------------------------------------------------------
    def get_all_available_manga_list(self):
        """ Returns the list of all mangas available on the mangaFox website (after an online search)

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
            TODO
        """

        results = []
        list_pages = []
        # Mangas are split letter by letter in the website
        for letter in "abcdefghijklmnopqrstuvwxyz":
            url_letter = self.url_search + letter + "/"
            soup = self.get_soup(url_letter)
            if soup is None:
                continue
            try:
                pages = soup.find("div", {"class": "read_more"}).find_all("li")
                for page in pages:
                    page = page.find("a")
                    link_page = page["href"]
                    list_pages.append(link_page)
            except:
                continue
        # Here, we have the full list of available pages referencing mangas
        print(list_pages)
        for link_page in list_pages:

            soup = self.get_soup(link_page)
            if soup is None: continue
            try:
                list_manga_on_page = soup.find_all("div", {"class":"content_grid_item_name"})
            except:
                continue

            for manga in list_manga_on_page:
                try:
                    manga = manga.find("a")
                    link_manga = manga["href"]
                    title_manga = manga["title"]

                    results.append({"title": title_manga, "link": link_manga})
                except:
                    continue

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

        # We get the soup related to the url
        soup = self.get_soup(url)
        if soup is None:
            return None

        # We look for a specific tag in the page
        try:

            results = soup.find_all("div", {"class": "chapter_number"})[1:] # the first one is unuseful

        except Exception as e:
            self.print_v("impossible to fin the 'div' tag in the webpage from ", url, ": ", str(e))
            return None

        # we extract titles, number of the volume....
        try:
            result_list = []
            for page in results:
                page = page.find("a")
                title = page.text.strip()
                chapter_and_number = title[len("Chapter "):]
                number = chapter_and_number.split(":")[0].strip()
                # We need to handle decimal valued chapters
                result_list.append({"link": page["href"], "title": title, "num": number}) # we take the first number
        except Exception as e:
            self.print_v("Impossible to get proper numbers from the html page ", url, ": ", str(e))
            return None

        result_list = sorted(result_list, key=lambda i: i['num'])

        # We need the correct title as mentionned in the page
        try:
            title = soup.find_all("h1")[-1].text
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
            list_pages_found = soup.find_all("img", {"class": "load_img"})
        except Exception as e:
            self.print_v("Impossible to get the 'img' tag in the page ", url, ": ", str(e))
            return None

        # We create the list of pages that are linked to this chapter
        pages = []
        try:
            for page in list_pages_found:
                link = page["src"]
                num = link.rsplit("/", 1)[-1].split(".")[0]
                pages.append({"link": link, "num": num})
        except Exception as e:
            self.print_v("Impossible to get the 'alt' or 'Page' or 'link' tag in the page ", url, ": ", str(e))
            return None



        # We get general manga info as name, number of the chapter, manga_title, number max of pages
        try:
            section = soup.find("div", {"class": "breadcrumb_custom"})
            chapter_full_title = section.find_all("li")[-1].text
            chapter_num = chapter_full_title.split(":",1)[0][len("Chapter "):]
            manga_title = section.find_all("li")[-2].text
            chapter_name = chapter_full_title.split(":")[1].strip()
            max_page = int(pages[-1]["num"])

        except Exception as e:
            self.print_v("Impossible to get tags 'alt' or 'Chapter'", ": ", str(e))
            return None

        return {"manga_title": manga_title, "chapter_num": chapter_num, "max_pages": max_page, "pages": pages}

    # SWITCH --------------------------------------------------------------------------------------
    def switch(self, search_word, selection="*", directory=""):
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
