from Engine.engine import Engine
import bs4
import os
import requests
import urllib.request
import math
import time
import aiohttp
import asyncio
import aiofiles as aiof

class EngineMangas(Engine):
    """
    The super Class `EngineMangas` is not designed to be instanciated, but to be inherited from.

    It binds every engine that deals with mangas.
        The functions defined here perform web and I/O tasks.
    """

    def __init__(self):
        """
        Attributes:
            category (string): category of the Engine; (here, manga).
            Make it easier for the core to sort engines by category.
        """
        super().__init__()
        self.category = "Manga"

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
            self.r = requests.get(url, stream = False,  headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})  # maybe speed up requests
            self.print_v("requests time: ", str(time.clock() - t))

            if self.r.status_code != 200:
                return False

            with open(save_path_file, 'wb') as flux:
                flux.write(self.r.content)

            time.sleep(0.1)
            return True

        except Exception as exception:
            self.print_v(str(exception))
            return False

    def async_download_pictures(self, url_list, save_path_file_list):

        async def get(url):
            """
            Make an async requests and returns the byte response content
            Args:
                url (string): url of the file

            Returns:
                response.read()(byte): content of the webpage
                or None if there is an error.
            """
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.read()
                    self.print_v(response.status)
                    return None

        async def save(path, content):
            """
            Save the content in the path asynchronously

            Args:
                path (string): path of the saving location
                content (byte): byte content that will be saved

            Return:
                results (list): list of booleans, True if no error or if the content is None, False else
            """

            if content == None:
                return False
            try:
                async with aiof.open(path, 'wb') as afp:
                    await afp.write(content)
                    await afp.flush()
                return True
            except:
                return False

        if len(url_list) != len(save_path_file_list):
            return None
        try:
            loop = asyncio.get_event_loop()
            self.print_v("lauching gets")
            results = loop.run_until_complete(asyncio.gather(*[get(url) for url in url_list]))
            self.print("launching saving")
            results = loop.run_until_complete(asyncio.gather(*[save(save_path_file_list[i], results[i]) for i in range(len(url_list))]))
        except Exception as e:
            self.print_v("Impossible to make the async download, an error occurred: ", str(e))
            return [ False for _ in range(len(url_list))]

        return results

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
                        os.rename(old_path, new_path)

        except Exception as e:
            print("impossible to rename the files: ", str(e))
            return False

        return True
