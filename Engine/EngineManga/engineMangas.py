import os
from abc import abstractmethod
import bs4
import requests
import urllib.request
import math
import time
import aiohttp
import asyncio
import aiofiles as aiof
import zipfile
import img2pdf

from Engine.engine import Engine
from typing import List, Optional, Union, Any
from Engine.EngineManga.manga import Manga, Chapter, Volume


class EngineMangas(Engine):
    """
    The super Class `EngineMangas` is not designed to be instanciated, but to be inherited from.

    It binds every engine that deals with mangas.
        The functions defined here performs web and I/O tasks.
    """

    def __init__(self):
        super().__init__()
        self.category = "Manga"  # category (string): category of the Engine; (here, manga).
        self.break_time = 0.1
        self.session = None
        self.list_manga_path = None

    # GET -----------------------------------------------------------------------------------------
    def get_soup(self, url: str, cookies=None) -> bs4.BeautifulSoup:
        """Creates a soup from an url with lxml parser. Returns a soup object if possible. None else
        Args:
            url (string): url of the webpage that will be turned into a soup
            cookies (dict): dictionnary of cookies

        Returns:
            soup (soup): A beautifulSoup soup object of the page
            None (None): if there is an error

        Raises:
            Doesn't raise an error but return None if there is a dl or soup creation.
            print_v() the error
        """
        cookies = cookies if cookies is not None else {}

        self.print_v("Trying to get the web page",  url)
        try:

            if self.session is None:
                self.session = requests.Session()

            r = self.session.get(url, cookies=cookies)
            if r.status_code == 200:
                soup = bs4.BeautifulSoup(r.content, features="lxml")
                return soup
        except Exception as e:
            try:
                self.print_v("Error: ", str(e), "with error code ", r.status_code)
                return None
            except Exception as _:  # the r value doesn't exist yet
                self.print_v("Error: ", str(e), ". Impossible to get a status code from the requests")
                return None

    def save_html(self, url: str, path: str) -> None:
        """Save the html from a webpage using requests library
        Args:
            url (string): url of the webpage that will be saved
            path (string): where to save the html page

        Returns:
            bool (bool): True if no error, False else

        Raises:
            Doesn't raise an error but return None if there is a dl or soup creation.
            print_v() the error
        """
        try:
            soup = self.get_soup(url)
            with open(path, "w", encoding="utf8") as flux:
                for line in soup.prettify():
                    flux.write(line)
        except Exception as e:
            self.print_v("An error occured while saving the webpage from this url: ", url, " see: ", str(e))

    def save_mangas_list_json(self, mangas_list: List[Manga], file_path: str):
        try:
            json_info_list = []

            for manga in mangas_list:
                json_info_list.append(manga.to_json())

            return self.save_json_file(json_info_list, file_path)

        except Exception as e:
            self.print_v("impossible to save in json file ", file_path, " : ", str(e))
            return False

    def find_manga_by_name(self, name: str, search_online = False) -> Optional[List[Manga]]:
        """ Searches a 'manga' by its name in the database.
        If not found, makes a requests, updates the config, and searches it again
            It returns every manga that has the name field in its title.
        Args:
            name (string): name of the required manga

        Returns:
            results (list): A list of manga objects

            empty list if no manga corresponds to the the name searched
        """

        self.print_v("find_manga_by_name: " + name)

        # list of found mangas
        results = []
        found = False

        # first, we search the name in the database
        raw_list_manga = self.get_json_file(self.list_manga_path)

        if raw_list_manga is None:
            list_manga = []

        try:
            list_manga = []
            for raw_manga in raw_list_manga:
                manga = Manga()
                manga.from_json(raw_manga)
                list_manga.append(manga)
        except Exception as e:
            list_manga = []

        for manga in list_manga:
            if name.lower() in manga.name.lower():
                found = True
                results.append(manga)

        # If the manga is not in the database, we look for it online (only if we use the 'online' mode
        if not found and search_online:
            self.print_v("searching online " + name)

            # update the list
            list_manga = self.get_all_available_manga_online_list()
            if list_manga == []:
                return []

            # save the list in the file
            self.save_mangas_list_json(list_manga, self.list_manga_path)
            for manga in list_manga:
                if name.lower() in manga.name.lower():
                    results.append(manga)

        return results

    def get_manga_info_from_name(self, name: str) -> Optional[Manga]:
        """
        Gets the list of all volumes from a manga name (analyze the first manga found)

        Args:
            name (string): name of the manga

        Returns:
            list_volume (list): List of Volumes
            None (None): None if there is an error
        """

        results = self.find_manga_by_name(name)
        if results == []:
            return None

        chosen_manga = results[0]
        url = chosen_manga.link

        retrieved_manga = self.get_manga_info_from_url(url)
        return retrieved_manga

    # abstract
    @abstractmethod
    def get_all_available_manga_online_list(self) -> Optional[List[Manga]]:
        pass

    @abstractmethod
    def get_manga_info_from_url(self, url: str) -> Optional[Manga]:
        pass

    @abstractmethod
    def get_info_from_chapter_url(self, url: str) -> Optional[Chapter]:
        pass

    # DOWNLOAD ------------------------------------------------------------------------------------
    # picture -----
    def download_picture(self, url: str, save_path_file: str) -> bool:
        """ Download a binary file.
        Here we use urllib, that seems to be a lot faster than requests on some manga websites.
        However, it's less secure.
        Args:
            url (string): url of the file that need to be downloaded.
            save_path_file (string): where to save the file after the download.

        Returns:
            bool (bool): True, if the download was a sucess, False instead.

        Raises:
            if an error occurred, print the exception to the log with self.print_v().

        Examples:
            >>> EngineMangas().download_picture("www.your_picture.png", "C:Users/your/path/to/file.png")
        """

        url = url.strip()
        try:
            r = urllib.request.urlopen(url)

            with open(save_path_file, "wb") as flux:
                flux.write(r.read())
            return True

        except Exception as exception:
            self.print_v(str(exception))
            return False

    def safe_download_picture(self, url: str, save_path_file: str) -> bool:
        """ Download a binary file.
        Here we use requests, that seems to be safer than urllib
        Args:
            url (string): url of the file that need to be downloaded.
            save_path_file (string): where to save the file after the download.

        Returns:
            bool (bool): True, if the download was a sucess, False instead.

        Raises:
            if an error occurred, prints the exception to the log with self.print_v().

        Examples:
            >>> EngineMangas().safe_download_picture("www.your_picture.png", "C:Users/your/path/to/file.png")
        """

        try:
            t = time.clock()
            url = url.strip()
            r = requests.get(url, stream=False,  headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})  # maybe speed up requests
            self.print_v("requests time: ", str(time.clock() - t))

            if r.status_code != 200:
                return False

            with open(save_path_file, 'wb') as flux:
                flux.write(r.content)

            time.sleep(self.break_time)
            return True

        except Exception as e:
            self.print_v(str(e))
            return False

    def async_download_pictures(self, url_list: List[str], save_path_file_list: List[str]):
        """ Async download files from the url_list and save it to save_path_file_list.

                Args:
                    url_list (list): list of the url of the file that need to be downloaded.
                    save_path_file_list (list): where to save the file after the download.

                Returns:
                    results (list): a list of True, if the download was a sucess, False instead. Returns a single False if the list are incompatible

                Raises:
                    if an error occured, print the exception to the log with self.print_v().
        """
        self.print_v( "async_download_pictures ", " ".join(url_list), " ".join(save_path_file_list))

        async def get_and_save(url, path):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            content = await response.read()
                        else:
                            return False
            except Exception as e:
                # requests error
                self.print_v("impossible to download the file ", url, " : ", str(e))
                return False

            try:
                self.print_v(path, " of ", url)
                async with aiof.open(path, 'wb+') as afp:
                    await afp.write(content)
                    await afp.flush()
                    return True
            except Exception as e:
                self.print_v("impossible to save the file: ", str(e))
                # saving error
                return False

        if len(url_list) != len(save_path_file_list):
            return False

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop) # TODO, verify if the new thread can be avoided to be create
            results = loop.run_until_complete(asyncio.gather(*[get_and_save(url_list[i].strip(), save_path_file_list[i]) for i in range(len(url_list))]))
            return results

        except Exception as e:
            self.print_v("Impossible to make the async download, an error occurred: ", str(e))
            return [False for _ in range(len(url_list))]

    # chapter -----
    def download_chapter(self, url: str, folder_path=None) -> bool:
        """ Download all images from the manga chapter page, rename them (purification) and download them in the folder_path
        ARGS:
            url (str): url of the given chapter. example "https://www.lelscan-vf.com/manga/the-promised-neverland/132"
            folder_path (string): default, default dl path. Path of the folder where images are downloaded.

        Returns:
            bool (bool): True if no error, False else

        Raises:
             Doesn't raise an error.

        Examples:
            EngineMangas().download_chapter("https://urlofmyfavoritemanga", "C://Users/JONHDOE/folder/" )
        """

        self.print_v("download_chapter...")

        if folder_path is None:
            folder_path = self.dl_directory

        # We retrieve info from the chapter
        retrieved_chapter = self.get_info_from_chapter_url(url)
        if retrieved_chapter == []:
            return False

        # We create the download directory
        create_directory = self.make_directory(folder_path)
        if create_directory is False:
            return False

        # Unpacking values
        pages = retrieved_chapter.pages_list
        chapter_num = retrieved_chapter.number
        # max_pages = results_chapter_page["max_pages"]
        manga_title = retrieved_chapter.manga_name


        for page in pages:
            link = page.link
            number = page.number
            extension = link.rsplit(".")[-1].strip()

            file_name = manga_title + "_" + str(chapter_num) + "_" + str(number) + "." + extension
            file_name = self.purify_name(file_name)
            save_name = os.path.join(folder_path, file_name)

            # here, we finally download the picture
            self.safe_download_picture(link, save_name)
            time.sleep(self.break_time)

        return True

    def async_download_chapter(self, url: str, folder_path=None, rename_auto=True, create_subFolder=False) -> bool:
        """ Download all images from the manga chapter page, rename them (purification) and download them
            If create_subFolder is True, the files will be stored in a subFolder with the name found on the website

        ARGS:
            url (str): url of the given chapter.
            folder_path (string): default, default dl path. Path of the folder where images are downloaded.
            rename_auto (bool): decides if the files should be renamed by adding 0: 1,2,9,11 -> 01,02,09,11
            create_subFolder (bool): True a subfolder named with the chapter name found on website, False directly in folder_path

        Returns:
            bool (bool): True if no error, False else

        Raises:
             Doesn't raise an error.

        Examples:
            TODO
        """

        self.print_v("async_download_chapter")

        if folder_path is None:
            folder_path = self.dl_directory

        # We retrieve info from the chapter
        retrieved_chapter = self.get_info_from_chapter_url(url)
        if retrieved_chapter is None:
            return False

        # Unpacking values
        pages = retrieved_chapter.pages_list
        chapter_num = retrieved_chapter.number
        # max_pages = results_chapter_page["max_pages"]
        manga_title = retrieved_chapter.manga_name

        # We create the download directory
        create_directory = self.make_directory(folder_path)
        if create_directory is False:
            return False

        if create_subFolder:
            folder_path = os.path.join(folder_path, manga_title+"_"+chapter_num)

            # creating the subFolder
            create_directory = self.make_directory(folder_path)
            if create_directory is False:
                return False


        url_list = []
        save_path_file_list = []
        file_name_list = []
        for page in pages:
            link = page.link
            number = page.number
            extension = link.rsplit(".")[-1].strip()

            file_name = manga_title + "_" + str(chapter_num) + "_" + str(number) + "." + extension
            file_name = self.purify_name(file_name)
            file_name_list.append(file_name)
            save_name = os.path.join(folder_path, file_name)

            # here, we finally download the picture
            url_list.append(link)
            save_path_file_list.append(save_name)

        time.sleep(self.break_time)

        results = self.async_download_pictures(url_list, save_path_file_list)
        for elem in results:
            if elem == False:
                return False

        # here everything were perfect. We can rename mangas.

        if rename_auto:
            self.print_v("Renaming in..." + folder_path)
            self.print_v("".join(file_name_list))
            success = self.rename_file_from_list(folder_path, file_name_list, display_only=False)

            if not success:
                self.print_v("impossible to rename files in "  + folder_path)
                return False
        return True

    def download_range_chapters_from_name(self, name: str, first: int, last: int,
                                          volume_name: str, folder_path=None, compress=None, rename_auto=True)-> Union[List[bool], bool]:
        self.print_v("download_range_chapters_from_url...")
        manga_list = self.find_manga_by_name(name)
        if manga_list is None:
            return False
        first_manga = manga_list[0]
        url = first_manga.link

        return self.download_range_chapters_from_url(url, first, last, volume_name, folder_path, compress)

    def download_range_chapters_from_url(self, url: str, first: int, last: int, folder_name: str, folder_path=None, compress=None, rename_auto=True) -> Union[List[bool], bool]:
        """
        Download a range of chapters, from first to last included in a folder volume_name. You need to add the number of the volume

        :param url:
        :param first:
        :param last:
        :param folder_name:
        :param folder_path:
        :param compress:
        :return:
        """

        self.print_v("download_range_chapters_from_url...")
        retrieved_manga = self.get_manga_info_from_url(url)
        if retrieved_manga is None:
            return False

        chapters_list = retrieved_manga.get_all_chapters()
        if chapters_list == []:
            return False

        results = []
        if folder_path is None:
            folder_path = self.dl_directory

        self.print_v('using the dl folder ' + folder_path)

        manga_directory = os.path.join(folder_path, retrieved_manga.name)
        volume_directory = os.path.join(manga_directory, folder_name)
        volume_directory = self.purify_name(volume_directory)

        for chap_number in range(first, last + 1): # we include the last one
            for chapter in chapters_list:
                if chap_number == chapter.number:
                    results.append(self.async_download_chapter(chapter.link, folder_path=volume_directory))
                    break


        if rename_auto:
            self.rename_file_from_folder_lexico(volume_directory, display_only=False)

        if compress:
            self.compress_folder(volume_directory, compress)

        return results

    # volume -----
    def download_volume(self, volume: Volume, folder_path: str, async_mode=True, rename_auto=True) -> bool:
        for chapter in volume.chapters_list:
            if async_mode:
                self.async_download_chapter(url=chapter.link, folder_path=folder_path, rename_auto=rename_auto)
            else:
                self.download_chapter(url=chapter.link, folder_path=folder_path)
        return True

    def download_volume_from_manga_name(self, name: str, number: int, folder_path=None, volume_name=None,
                                        rename_auto=True, compress=None, async_mode = True, display_only=True) -> bool:
        """
        Download a single volume just with the name of a manga
        Args:
            name (string): name of the manga
            number (string): number of the volume to be downloaded (maybe rename it to volume)
            folder_path (string): where to save the chapter. Default, dl
            volume_name (string): Renaming the volume if necessary
            rename_auto (bool): decides if the files should be renamed by adding 0: 1,2,9,11 -> 01,02,09,11
            display_only (bool) : True if the function is just used to verify if the manga exist, False to directly download
            compress (string) : extension of the compress file (with the dot)

        Returns:
            bool (bool): False if the manga cannot be downloaded, list of bool if the donwload pass th esaync part

        Raises:
            None, but print_v() problems.

        """
        self.print_v("download_volume_from_manga_name...")
        manga_list = self.find_manga_by_name(name)
        if manga_list is None:
            return False
        first_manga = manga_list[0]
        self.print_v("download_volume_fom_manga: first manga: " + str(first_manga))

        results = self.download_volume_from_manga_url(
            url = first_manga.link,
            number = number,
            folder_path = folder_path,
            volume_name = volume_name,
            rename_auto = rename_auto,
            display_only = display_only,
            async_mode = async_mode,
            compress = compress)

        return results

    def download_last_volume_from_manga_name(self, name: str, folder_path=None, volume_name=None,rename_auto=True,
                                             compress=".cbz", async_mode=True, display_only=True) -> bool:
        """
            Download a single volume just with the name of a manga
            Args:
                name (string): name of the manga
                folder_path (string): where to save the chapter. Default, dl
                display_only (bool) : True if the function is just used to verify if the manga exist, False to directly download

            Returns:
                bool (bool): False if the manga cannot be downloaded, list of bool if the donwload pass th esaync part

            Raises:
                None, but print_v() problems.

        """

        self.print_v("download_last_volume_from_manga_name...")
        manga_list = self.find_manga_by_name(name)
        if manga_list is None:
            return False
        first_manga = manga_list[0]


        retrieved_manga = self.get_manga_info_from_url(first_manga.link)
        volumes_list = retrieved_manga.volumes_list
        last_Volume = volumes_list[0]

        if volume_name is None:
            folder_name = last_Volume.name + "_" + str(last_Volume.number)
        else:
            folder_name = volume_name

        if folder_path is None:
            folder_path = self.dl_directory

        manga_directory = os.path.join(folder_path, retrieved_manga.name)
        volume_directory = os.path.join(manga_directory, folder_name)
        volume_directory = self.purify_name(volume_directory)


        self.print_v("last volume found: " + str(last_Volume))

        if display_only:
            print("If you want to really make it, launch this function again with display_only = False")
            return True

        result = self.download_volume(volume = last_Volume, folder_path=volume_directory,
                                      async_mode=async_mode, rename_auto=rename_auto)

        if rename_auto:
            self.rename_file_from_folder_lexico(folder_directory=volume_directory, display_only=False)

        if compress:
            self.compress_folder(folder_path= volume_directory, ext=compress)

        return result

    def download_volume_from_manga_url(self, url:str, number:int, folder_path=None, volume_name=None,
                                       rename_auto=True, compress=None, async_mode=True, display_only=True) -> bool:
        """
            Download a single volume just with the url of a manga
            Args:
                url (string): url of the manga
                number (string): number of the volume to be downloaded (maybe rename it to volume)
                folder_path (string): where to save the chapter. Default, dl
                display_only (bool) : True if the function is just used to verify if the manga exist, False to directly download
                compress (string) : extension of the compress file (with the dot)
            Returns:
                bool (bool): False if the manga cannot be downloaded, list of bool if the donwload pass th esaync part

            Raises:
                None, but print_v() problems.
        """

        self.print_v("download_volume_from_manga_url...")
        retrieved_manga = self.get_manga_info_from_url(url)
        if retrieved_manga is None:
            return False

        self.print_v(str(retrieved_manga.volumes_list))

        volume_list = retrieved_manga.volumes_list
        if volume_list == []:
            return False

        found = False
        found_volume: Optional[Volume] = None
        for volume in volume_list:
            if volume.number == number:
                found = True
                found_volume = volume
                break

        if not found:
            return False

        self.print_v("manga found ", str(found_volume.name))

        if display_only:
            print("If you want to really make it, launch this function again with display_only = False")
            return True

        if volume_name is None:
            folder_name = retrieved_manga.name + "_V" + str(found_volume.number)
        else:
            folder_name = volume_name

        if folder_path is None:
            folder_path = self.dl_directory
        manga_directory = os.path.join(folder_path, retrieved_manga.name)
        volume_directory = os.path.join(manga_directory, folder_name)
        volume_directory = self.purify_name(volume_directory)

        self.print_v("trying to download volume from manga url \n" + folder_name + "\n" + volume_directory)

        # we avoid renaming each chapter
        results = self.download_volume(found_volume, volume_directory, async_mode=async_mode, rename_auto=False)

        # we rename then all at once
        if rename_auto:
            self.rename_file_from_folder_lexico(folder_directory=volume_directory, display_only=False)

        if compress:
            self.compress_folder(folder_path= volume_directory, ext=compress)

        return results

    # manga -----
    def download_whole_manga_from_name(self, name: str, folder_path=None, async_mode=False, compress=None, rename_auto=True) -> bool:
        self.print_v("download_whole_manga_from_name...")
        mangas = self.find_manga_by_name(name)
        first_manga = mangas[0]
        url = first_manga.link
        return self.download_whole_manga_from_url(url = url, folder_path=folder_path, async_mode=async_mode,
                                                  compress=compress, rename_auto=rename_auto)


    def download_whole_manga_from_url(self, url: str, folder_path=None, async_mode=True, compress=None, rename_auto=True) -> bool:
        """ Download all images from the manga main page, rename them (purification) and download them
        TODO: REWORK THIS FUNCTION
        ARGS:
            url (str): url of the given manga.
            folder_path (string): default, default dl path. Path of the folder where images are downloaded.

        Returns:
            bool (bool): True if no error, False else

        Raises:
            Doesn't raise an error.

        """
        print("compress", compress)

        self.print_v("download_whole_manga_from_url")
        # We gather main manga page info
        retrieved_manga: Manga = self.get_manga_info_from_url(url)
        if retrieved_manga is None:
            return False

        if folder_path is None:
            folder_path = self.dl_directory

        # directory for all the content linked with this very manga (chapters, volumes)
        manga_directory = os.path.join(folder_path, retrieved_manga.name)

        # Download chapters not in a specified volume (a lot of website don't make a difference)
        chapters: List[Chapter] = retrieved_manga.chapters_without_volumes_list
        for chapter in chapters:
            folder_name = retrieved_manga.name + "_" + str(chapter.number)
            chapter_directory = os.path.join(manga_directory, folder_name)
            chapter_directory = self.purify_name(chapter_directory)

            if async_mode:
                self.async_download_chapter(url=chapter.link, folder_path=chapter_directory)
            else:
                self.download_chapter(url=chapter.link, folder_path=chapter_directory)
            if rename_auto:
                self.rename_file_from_folder_lexico(chapter_directory, display_only=False)

            if compress:
                self.compress_folder(chapter_directory, compress)

        volumes: List[Volume] = retrieved_manga.volumes_list
        for volume in volumes:
            folder_name = retrieved_manga.name + "_V" + str(volume.number)
            volume_directory = os.path.join(manga_directory, folder_name)
            self.download_volume(volume=volume, folder_path=volume_directory, async_mode=async_mode)
            if rename_auto:
                self.rename_file_from_folder_lexico(volume_directory, display_only=False)
            if compress:
                self.compress_folder(volume_directory, compress)


        return True


    # RENAMING ------------------------------------------------------------------------------------
    def lexicographical_list_converter(self, name_list, sep="_") -> Union[List[Union[str, Any]], None]:
        """ Returns a list of name where number are adjusted with lexicographical order

        Args:
            name_list (list): List of all the names that need to be changed
            sep (string): The default separator used to detect numbers

        Returns:
            name_with_extension_list (list): List of all names rewritten with lexicographical order
            None (None): Returns None if error

        Raises:
            Doesn't raise an error.
            print a warning with self.print_v() and return None

        Example:
            e.lexicographical_list_converter(["a_50_1.jpg", "a_1_8.png", "a_300_30.bmp"])
            ['a_050_01.jpg', 'a_001_08.png', 'a_300_30.bmp']
        """

        try:
            # First we separate the name from it's extension
            split_name_list = [file.rsplit(".", 1) for file in name_list]
            # Then, we separate every part of the names according to the chosen separator
            split_radical_on_sep_list = [split_name[0].split(sep) for split_name in split_name_list]

            # We check if every name has the same 'structure'
            reference_size = len(split_radical_on_sep_list[0])
            print(split_radical_on_sep_list)
            for split_radical in split_radical_on_sep_list:
                if len(split_radical) != reference_size:
                    self.print_v("All the names in name_list must have the same format: ")
                    return None

        except Exception as e:
            self.print_v("The name_list variable as a problem: ", str(e))
            return None

        try:
            # We select the first element of the list that will be used to know where digits are.
            index_list = []
            reference_name = split_radical_on_sep_list[0]
            for i in range(len(reference_name)):
                if reference_name[i].isdigit():
                    index_list.append(i)
                # we can also deal with float
        except Exception as e:
            self.print_v("Error while extracting numbers from the names,"
                         "perhaps there is an unsupported float: ", str(e))
            return None

        try:
            # We now have a list of all indexes where there are numbers
            # we need to get the max number corresponding to all indexes
            max_list = []
            for index in index_list:
                # list of all number of all split name at the given index
                number_at_index_list = [int(split_radical[index]) for split_radical in split_radical_on_sep_list]
                max_list.append(max(number_at_index_list))

            # for all indexes that are number, we add 0 to get a constant size.
            for i in range(len(index_list)):
                index = index_list[i]
                max_number = max_list[i]
                # we get the size of the max number: faster than len(str(max_number))
                max_size = int(math.log10(max_number)) + 1
                for split_radical in split_radical_on_sep_list:
                    split_radical[index] = "0" * (max_size - len(split_radical[index])) + split_radical[index]
        except Exception as e:
            self.print_v("Error while adding zero to the names: ", str(e))
            return None

        try:
            # Finally, we reconstruct the names by adding the separator and the extension
            name_with_extension_list = []
            for i in range(len(split_name_list)):
                radical = sep.join(split_radical_on_sep_list[i])
                # We add the extension at the end of the radical
                name_with_extension = radical + "." + split_name_list[i][-1]
                name_with_extension_list.append(name_with_extension)
        except Exception as e:
            self.print_v("Error while dealing with the extensions, maybe a file has no extensions?: ", str(e))
            return None

        return name_with_extension_list

    def rename_file_from_list(self, folder_directory: str, name_list: List[str], display_only=True) -> bool:
        """ Rename every files in a folder that match with a name_list

            Args:
                folder_directory (string): Path of the folder where files need to be renamed
                name_list (list): list of files that need to be renamed
                display_only (bool): default True.
                    If True, just print the changes, else, execute the modificationand rename all the files in the folder

            Returns:
                bool (bool): True if no error, False else

            Raises:
                Doesn't raise an error.
                print a warning.
            """


        lexico_files = self.lexicographical_list_converter(name_list)
        if lexico_files is None:
            return False

        try:
            for i in range(len(lexico_files)):
                old_file = name_list[i]
                new_file = lexico_files[i]
                old_path = os.path.join(folder_directory, old_file)
                new_path = os.path.join(folder_directory, new_file)
                if display_only:
                    print(old_path, " -> ", new_path)
                else:
                    if old_file != new_file:
                        os.rename(old_path, new_path)

        except Exception as e:
            print("impossible to rename the files: ", str(e))
            return False

        return True

    def rename_file_from_folder_lexico(self, folder_directory: str, display_only=True) -> bool:
        """ Rename every files in a folder to get a lexicographical order list of files

        Args:
            folder_directory (string): Path of the folder where files need to be renamed
            display_only (bool): default True.
                If True, just print the changes, else, execute the modificationand rename all the files in the folder

        Returns:
            bool (bool): True if no error, False else

        Raises:
            Doesn't raise an error.
            print a warning.
        """
        self.print_v("rename_file_from_folder_lexico")
        try:
            files = os.listdir(folder_directory)
            if files == []:
                return True
        except Exception as e:
            self.print_v("impossible to analyze ", folder_directory, " folder. Maybe it's a wrong path: ", str(e))
            return False

        lexico_files = self.lexicographical_list_converter(files)
        if lexico_files is None:
            return False

        try:
            for i in range(len(files)):
                old_file = files[i]
                new_file = lexico_files[i]
                old_path = os.path.join(folder_directory, old_file)
                new_path = os.path.join(folder_directory, new_file)
                if display_only:
                    print(old_path, " -> ", new_path)
                else:
                    if old_file != new_file:
                        try:
                            os.rename(old_path, new_path)
                        except Exception as e:
                            print("impossible to rename ", old_path, " to ", new_path + ":" + str(e))

        except Exception as e:
            print("impossible to rename the files: ", str(e))
            return False

        return True

    # ZIP -----------------------------------------------------------------------------------------

    def compress_folder(self, folder_path: str, ext=".cbz") -> bool:
        self.print_v("compress_folder...")
        if ext == ".cbz" or ext == ".zip":
            return self.compress_CBZ(folder_path, ext)
        elif ext == ".pdf":
            return self.compress_PDF(folder_path)
        else:
            print("I cannot deal with " + ext + " files")
            return False

    def compress_CBZ(self, folder_path: str, ext=".cbz") -> bool:
        """"Compress A folder in zip format. Add a zip like extension like .zip, .cbz
        Args:
            folder_path (string): path of the directory that will be compressed
            ext (string): (optional) extension added to the folder name
        Returns:
            bool (bool): True if everything is correct, False if there is an error or if the folder is empty
        Raises:
            Raises nothing but print_v() errors
        """
        self.print_v("compress_CBZ...")
        try:
            files = os.listdir(folder_path)
            if files == []:
                return False
        except Exception as e:
            self.print_v("impossible to analyze ", folder_path, " folder. Maybe it's a wrong path: ", str(e))
            return False

        try:
            for i in range(len(files)):
                files[i] = os.path.join(folder_path, files[i])
        except Exception as e:
            self.print_v("error while joining names ", str(e))
            return False

        try:
            zip_file = zipfile.ZipFile(folder_path + ext, 'w')
            with zip_file:
                # writing each file one by one
                for file in files:
                    zip_file.write(file)
            return True
        except Exception as e:
            self.print_v("impossible to compress ", folder_path, " folder", str(e))
            return False

    def compress_PDF(self, folder_path: str) -> bool:
        """"Create a pdf of all pictures in a folder
        Args:
            folder_path (string): path of the directory that will be compressed
        Returns:
            bool (bool): True if everything is correct, False if there is an error or if the folder is empty
        Raises:
            Raises nothing but print_v() errors
        """

        self.print_v("compress_PDF...")
        try:
            files = os.listdir(folder_path)
            if files == []:
                return False
        except Exception as e:
            self.print_v("impossible to analyze ", folder_path, " folder. Maybe it's a wrong path: ", str(e))
            return False

        try:
            for i in range(len(files)):
                files[i] = os.path.join(folder_path, files[i])
        except Exception as e:
            self.print_v("error while joining names ", str(e))
            return False

        try:
            with open(folder_path + ".pdf", "wb") as f:
                print("here ***********************")
                f.write(img2pdf.convert(files))
            return True

        except Exception as e:
            self.print_v("impossible to turn into a pdf ", folder_path, " folder. ", str(e))
            return False