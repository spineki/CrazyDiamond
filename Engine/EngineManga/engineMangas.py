from Engine.engine import Engine
import bs4
import os
import requests
import urllib.request
import math


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
            r = requests.get(url, stream=False, headers={'Connection': 'close'})  # maybe speed up requests
            with open(save_path_file, "wb") as flux:
                flux.write(r.content)  # instead of r.content()
            return True

        except Exception as exception:
            self.print_v(str(exception))
            return False

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
                self.print_v("Error: ", str(e), "with error code ", r.status_code )
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


    def lexicographical_list_converter(self, name_list, sep ="_"):

        try:
            # First we separate the name from it's extension
            split_name_list = [file.rsplit(".", 1) for file in name_list]
            # Then, we separate every part of the names according to the chosen separator
            split_radical_on_sep_list = [split_name[0].split(sep) for split_name in split_name_list]

            # We check if every name has the same 'structure'
            reference_size = len(split_radical_on_sep_list)
            for split_radical in split_radical_on_sep_list:
                if len(split_radical) != reference_size:
                    self.print_v("All the names in name_list must have the same format: ")
                    return False

        except Exception as e:
            self.print_v("The name_list variable as a problem: ", str(e))
            return False

        # We select the first element of the list that will be used to know where digits are.
        index_list = []
        reference_name = split_radical_on_sep_list[0]
        for i in range(len(reference_name)):
            if reference_name[i].isdigit():
                index_list.append(i)
            # we can also deal with float

        # We now have a list of all indexes where are numbers
        # we need to get the max number corresponding to all indexes
        max_list = []
        for index in index_list:
            # list of all number of all split name at the given index
            number_at_index_list = [ int(split_radical[index]) for split_radical in split_radical_on_sep_list ]
            max_list.append(max(number_at_index_list))

        # for all indexes that are number, we add 0 to get a constant size
        for i in range(len(index_list)):
            index = index_list[i]
            max_number = max_list[i]
            # we get the size of the max number: faster than len(str(max_number))
            max_size = int(math.log10(max_number)) + 1
            for split_radical in split_radical_on_sep_list:
                split_radical[index] = "0" * (max_size - len(split_radical[index])) + split_radical[index]

        # finally, we reconstruct the names by adding the separator and the extension
        name_with_extension_list = []
        for i in range(len(split_name_list)):
            radical = sep.join(split_radical_on_sep_list[i])
            name_with_extension = radical + "." + split_name_list[i][-1] # we add the extension at the end of the radical
            name_with_extension_list.append(name_with_extension)

        return name_with_extension_list


    @staticmethod
    def rename_folder(path, sep="_"):
        """ Rename every files in a folder to get a lexicographical order list of files

        Args:
            path (string): Path of the folder where files need to be renamed
            sep (string): The default separator that will replace unauthorized characters

        Returns:
            bool (bool): True if no error, False else

        Raises:
            Doesn't raise an error.
            print a warning.

        Example:
            test
        """

        # get the list of all files in the given folder
        files = os.listdir(path)

        decompo_file = [file.rsplit(".", 1) for file in files]  # on a decompoFile[i][0] radical et  decompoFile[i][1] extension
        list_indice = []
        list_decompo = [file[0].split(sep) for file in decompo_file]

        example_decompo = list_decompo[0]
        for i in range(len(example_decompo)):
            if example_decompo[i].isdigit():
                list_indice.append(i)
        print(list_indice)
        # now, we the indice list for all the names that are linked to a number (of page, chapter, tome...)
        for indice in list_indice:
            # we get all the number cooresponding to the indice
            list_num = []
            for file in list_decompo:
                print(file)
                list_num.append(int(file[indice]))
            # we get the greatest
            max_number = max(list_num)
            size = len(str(max_number))
            for j in range(len(list_decompo)):
                # we add has many zeros as needed to make the number corresponding to a perfect ratio
                list_decompo[j][indice] = "0" * (size - len(str(list_decompo[j][indice]))) + str(
                    list_decompo[j][indice])

        new_files_without_ext = [sep.join(elem) for elem in list_decompo]
        new_files_with_ext = [new_files_without_ext[i] + "." + decompo_file[i][1] for i in
                              range(len(new_files_without_ext))]

        for i in range(len(files)):
            file_old = files[i]
            file_new = new_files_with_ext[i]
            print(file_old)
            print(file_new)

            if file_old != file_new:
                os.rename(path + "/" + file_old, path + "/" + file_new)