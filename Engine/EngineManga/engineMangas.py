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
from Engine.engine import Engine


class EngineMangas(Engine):
    """
    The super Class `EngineMangas` is not designed to be instanciated, but to be inherited from.

    It binds every engine that deals with mangas.
        The functions defined here performs web and I/O tasks.
    """

    def __init__(self):
        """
        Attributes:
            category (string): category of the Engine; (here, manga).
            Make it easier for the core to sort engines by category.
        """
        super().__init__()
        self.category = "Manga"
        self.break_time = 0.1

    # GET -----------------------------------------------------------------------------------------
    def get_soup(self, url):
        """Creates a soup from an url with lxml parser. Returns a soup object if possible. None else
        Args:
            url (string): url of the webpage that will be turned into a soup

        Returns:
            soup (soup): A beautifulSoup soup obejct of the page
            None (None): if there is an error

        Raises:
            Doesn't raise an error but return None if there is a dl or soup creation.
            print_v() the error
        """

        self.print_v("Trying to get the web page",  url)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                soup = bs4.BeautifulSoup(r.content, features="lxml")
                return soup
        except Exception as e:
            try:
                self.print_v("Error: ", str(e), "with error code ", r.status_code)
            except Exception as _:  # the r value doesn't exist yet
                self.print_v("Error: ", str(e), ". Impossible to get a status code from the resquests")

    def save_html(self, url, path):
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

    def find_manga_by_name(self, name):
        """ Searches a 'manga' by its name in the database. If not found, makes a requests, updates the config, and searches it again
            It returns every manga that has the name field in its title.
        Args:
            name (string): name of the required manga

        Returns:
            results (list): A list of dict with the following keys
            {
            title (string): Name of the manga
            link (string): url of the manga main page
            }

            None if no manga corresponds to the the name searched

        Examples:
            TODO
        """

        # list of found mangas
        results = []
        found = False

        # first, we search the name in the database
        list_manga = self.get_json_file(self.list_manga_path)
        if list_manga is None:
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
            if list_manga is None:
                return None
            # save the list in the file
            self.save_json_file(list_manga, self.list_manga_path)
            for manga in list_manga:
                if name.lower() in manga["title"].lower():
                    results.append(manga)

        if not results:
            return None
        return results

    def get_list_volume_from_manga_name(self, name):
        """
        Gets the list of all volumes from a manga name (analyze the first manga found)

        Args:
            name (string): name of the manga

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

        results = self.find_manga_by_name(name)
        if results is None or results == []:
            return None

        chosen_manga = results[0]
        url = chosen_manga["link"]

        list_volume = self.get_list_volume_from_manga_url(url)
        return list_volume

    # abstract
    @abstractmethod
    def get_all_available_manga_list(self):
        pass

    @abstractmethod
    def get_list_volume_from_manga_url(self, url):
        pass

    @abstractmethod
    def get_info_from_chapter_url(self, url):
        pass

    # DOWNLOAD ------------------------------------------------------------------------------------
    def download_picture(self, url, save_path_file):
        """ Download a binary file.
        Here we use urllib, that seems to be a lot faster than requests on some manga websites.
        However, it's less secure.
        Args:
            url (string): url of the file that need to be downloaded.
            save_path_file (string): where to save the file after the download.

        Returns:
            bool (bool): True, if the download was a sucess, False instead.

        Raises:
            if an error occured, print the exception to the log with self.print_v().

        Examples:
            >>> engineMangas = EngineMangas()
            >>> engineMangas.download_picture("www.your_picture.png", "C:Users/your/path/to/file.png")
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

    def safe_download_picture(self, url, save_path_file):
        """ Download a binary file.
        Here we use requests, that seems to be safer than urllib
        Args:
            url (string): url of the file that need to be downloaded.
            save_path_file (string): where to save the file after the download.

        Returns:
            bool (bool): True, if the download was a sucess, False instead.

        Raises:
            if an error occured, print the exception to the log with self.print_v().

        Examples:
            >>> engineMangas = EngineMangas()
            >>> engineMangas.safe_download_picture("www.your_picture.png", "C:Users/your/path/to/file.png")
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

    def async_download_pictures(self, url_list, save_path_file_list):
        """ Async download files from the url_list and save it to save_path_file_list.

                Args:
                    url_list (list): list of the url of the file that need to be downloaded.
                    save_path_file_list (list): where to save the file after the download.

                Returns:
                    results (list): a list of True, if the download was a sucess, False instead. Returns a single False if the list are incompatible

                Raises:
                    if an error occured, print the exception to the log with self.print_v().
        """
        print(url_list, save_path_file_list)

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
                print(path, " de ", url)
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
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(asyncio.gather(*[get_and_save(url_list[i].strip(), save_path_file_list[i]) for i in range(len(url_list))]))
            return results

        except Exception as e:
            self.print_v("Impossible to make the async download, an error occurred: ", str(e))
            return [False for _ in range(len(url_list))]

    def download_chapter(self, url, folder_path=None):
        """ Download all images from the manga chapter page, rename them (purification) and download them in the folder_path
        ARGS:
            url (str): url of the given chapter. example "https://www.lelscan-vf.com/manga/the-promised-neverland/132"
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

    def async_download_chapter(self, url, folder_path=None, rename_auto = True):
        """ Download all images from the manga chapter page, rename them (purification) and download them
        ARGS:
            url (str): url of the given chapter.
            folder_path (string): default, default dl path. Path of the folder where images are downloaded.

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
        file_name_list = []
        for page in pages:
            link = page["link"]
            number = page["num"]
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
            print("road to rename")
            print(folder_path)
            print(file_name_list)
            success = self.rename_file_from_list(folder_path, file_name_list, display_only=False)

            if not success:
                self.print_v("impossible to rename files in "  + folder_path)
                return False
        return True

    def download_volume_from_manga_name(self, name, number, folder_path=None, display_only=True):
        """
        Download a single volume just with the name of a manga
        Args:
            name (string): name of the manga
            number (string): number of the volume to be downloaded (maybe rename it to volume)
            folder_path (string): where to save the chapter. Default, dl
            display_only (bool) : True if the function is just used to verify if the manga exist, False to directly download

        Returns:
            bool (bool): False if the manga cannot be downloaded, list of bool if the donwload pass th esaync part

        Raises:
            None, but print_v() problems.

        """

        manga_list = self.find_manga_by_name(name)
        if manga_list is None:
            return False
        first_manga = manga_list[0]
        self.print_v("download_volume_fom_manga: first manga: " + str(first_manga))

        results = self.download_volume_from_manga_url(first_manga["link"], number, folder_path, display_only)

        return results

    def download_volume_from_manga_url(self, url, number, folder_path=None, display_only=True):
        """
            Download a single volume just with the url of a manga
            Args:
                url (string): url of the manga
                number (string): number of the volume to be downloaded (maybe rename it to volume)
                folder_path (string): where to save the chapter. Default, dl
                display_only (bool) : True if the function is just used to verify if the manga exist, False to directly download

            Returns:
                bool (bool): False if the manga cannot be downloaded, list of bool if the donwload pass th esaync part

            Raises:
                None, but print_v() problems.

        """

        volumes = self.get_list_volume_from_manga_url(url)
        if volumes is None:
            return False

        self.print_v(str(volumes))

        volume_list = volumes["chapter_list"]
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

        self.print_v("manga found ", str(found_volume))

        if display_only:
            return True

        folder_name = found_volume["title"] + "_V" + str(found_volume["num"])
        if folder_path is None:
            folder_path = self.dl_directory
        manga_directory = os.path.join(folder_path, volumes["title"])
        volume_directory = os.path.join(manga_directory, folder_name)
        volume_directory = self.purify_name(volume_directory)

        results = self.async_download_chapter(found_volume["link"], folder_path = volume_directory, rename_auto=True)
        #self.rename_file_from_folder_lexico(volume_directory, display_only = False)
        return results

    def download_range_chapters_from_name(self, name, first, last, volume_name, folder_path=None, compress=True):
        """
        WIP TODO
        Download a range of chapters, from first to last included in a folder volume_name. You need to add the number of the volume
        Args:
            name (string): name of the manga
            first (int): number of the first chapter
            last (int): number of the last chapter, included
            volume_name (string): name of the volume, where chapters will be mixed
            folder_path (string): where to save the chapter. Default, dl

        Returns:
            bool (bool): False if the manga cannot be downloaded, list of bool if the donwload pass the async part

        Raises:
            None, but print_v() problems.

        """

        manga_list = self.find_manga_by_name(name)
        if manga_list is None:
            return False
        first_manga = manga_list[0]
        url = first_manga["link"]

        volumes = self.get_list_volume_from_manga_url(url)
        if volumes is None:
            return False

        volume_list = volumes["chapter_list"]
        if volume_list == []:
            return False


        results = []
        if folder_path is None:
            folder_path = self.dl_directory
        manga_directory = os.path.join(folder_path, volumes["title"])
        folder_name = volume_name  # chosen by the reader
        volume_directory = os.path.join(manga_directory, folder_name)
        volume_directory = self.purify_name(volume_directory)

        for chap_number in range(first, last + 1):

            for volume in volume_list:
                if volume["num"] == chap_number:
                    found_volume = volume

                    results.append(self.async_download_chapter(found_volume["link"], folder_path=volume_directory))

                    break
        self.rename_file_from_folder_lexico(volume_directory, display_only=False)

        if compress:
            self.compress_folder(volume_directory)

        return results

    def download_last_volume_from_manga_name(self, name, folder_path=None, display_only=True):
        """
            Download a single volume just with the name of a manga
            Args:
                name (string): name of the manga
                number (string): number of the volume to be downloaded (maybe rename it to volume)
                folder_path (string): where to save the chapter. Default, dl
                display_only (bool) : True if the function is just used to verify if the manga exist, False to directly download

            Returns:
                bool (bool): False if the manga cannot be downloaded, list of bool if the donwload pass th esaync part

            Raises:
                None, but print_v() problems.

        """

        manga_list = self.find_manga_by_name(name)
        if manga_list is None:
            return False
        first_manga = manga_list[0]
        infos_manga = self.get_list_volume_from_manga_name(first_manga["title"])
        chapter_list = infos_manga["chapter_list"]
        last_chapter_title = chapter_list[0]["title"]
        manga_link = first_manga["link"]
        last_chapter_num = chapter_list[0]["num"]
        self.print_v("last chapter found: " + last_chapter_title + " : N°" + str(last_chapter_num))
        results = self.download_volume_from_manga_url(manga_link, last_chapter_num, folder_path, display_only)

        return results

    def download_manga_from_url(self, url, folder_path=None, async_mode=False):
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
            TODO
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

    def download_manga_from_name(self, name, folder_path = None, async_mode=False):
        mangas = self.find_manga_by_name(name)
        first_manga = mangas[0]
        url = first_manga["link"]
        return self.download_manga_from_url(url, folder_path, async_mode)

    # RENAMING ------------------------------------------------------------------------------------
    def lexicographical_list_converter(self, name_list, sep="_"):
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
            >>> e.lexicographical_list_converter(["a_50_1.jpg", "a_1_8.png", "a_300_30.bmp"])
            >>> ['a_050_01.jpg', 'a_001_08.png', 'a_300_30.bmp']
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

    def rename_file_from_list(self, folder_directory, name_list, display_only=True):
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

    def rename_file_from_folder_lexico(self, folder_directory, display_only=True):
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
    def compress_folder(self, dir_name, ext=".cbz"):
        """"Compress A folder in zip format. Add a zip like extension like .zip, .cbz
        Args:
            dir_name (string): path of the directory that will be compressed
            ext (string): (optional) extension added to the folder name
        Returns:
            bool (bool): True if everything is correct, False if there is an error or if the folder is empty
        Raises:
            Raises nothing but print_v() errors
        """

        try:
            files = os.listdir(dir_name)
            if files == []:
                return False
        except Exception as e:
            self.print_v("impossible to analyze ", dir_name, " folder. Maybe it's a wrong path: ", str(e))
            return False

        try:
            for i in range(len(files)):
                files[i] = os.path.join(dir_name, files[i])
        except Exception as e:
            self.print_v("error while joining names ", str(e))
            return False

        try:
            zip_file = zipfile.ZipFile(dir_name + ext, 'w')
            with zip_file:
                # writing each file one by one
                for file in files:
                    zip_file.write(file)
            return True
        except Exception as e:
            self.print_v("impossible to compress ", dir_name, " folder", str(e))
            return False
