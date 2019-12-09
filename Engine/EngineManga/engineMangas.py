from Engine.engine import Engine
import bs4
import os
import requests
import time
import urllib.request


class EngineMangas(Engine):
    """
    A class that binds every engine that deals with mangas
    """
    def __init__(self):
        super().__init__()
        self.category = "Manga"

    def download_picture(self, url, save_path_file):
        """ Download a binary file
        here we use urllib, that seems to be a lot faster than requests on manga websites.
        """
        t1 = time.clock()
        self.print_v("before download")
        try:
            r = urllib.request.urlopen(url)

            #r = requests.get(url, stream = False, headers = {'Connection': 'close'}) # maybe speed up requests
            self.print_v("after download", time.clock() - t1)
            with open(save_path_file, "wb") as flux:
                self.print_v('before writting')
                flux.write(r.read()) # instead of r.content()
            return True
        except Exception as exception:
            print(str(exception))
            return False


    def safe_download_picture(self, url, save_path_file):
        """ Download a binary file
                here we use request, that seems safer than urlib.
                """
        t1 = time.clock()
        self.print_v("before download")
        try:

            r = requests.get(url, stream = False, headers = {'Connection': 'close'}) # maybe speed up requests
            self.print_v("after download", time.clock() - t1)
            with open(save_path_file, "wb") as flux:
                self.print_v('before writting')
                flux.write(r.content)  # instead of r.content()
            return True
        except Exception as exception:
            print(str(exception))
            return False

    def get_soup(self, url):
        """Create a soup from an url. Return a soup object if possible. None else"""
        self.print_v("ici l'url dans le requests ", url)
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.content, features="lxml")
        return soup
        """
        except:
            if r.status_code == 200:
                print("erreur 200, on tente quand même un dl")
                return
            print("impossible to access ", url, "\nerror:", r.status_code)
            return None"""

    def save_html(self, url, path ="htmlsavedfromengine.html"):
        soup = self.get_soup(url)
        print(self.root_path + "/"+path)
        with open(self.root_path + "/"+ path, "w", encoding="utf8") as flux:
            for line in soup.prettify():
                flux.write(line)

    @staticmethod
    def rename_folder(path, sep="_"):
        # need a refactorization, better understanding and error handeling.
        if path == "":
            return False
        # penser a retirer les points
        # traitement au cas par cas des extensions, puis des tirets bas
        files = os.listdir(path)
        print(len(files), "to work on ")
        decompo_file = [file.rsplit(".", 1) for file in
                        files]  # on a decompoFile[i][0] radical et  decompoFile[i][1] extension
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