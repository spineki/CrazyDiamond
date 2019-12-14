import json
import os
from os.path import dirname
from PIL import Image

class Engine:
    """ The super Class `Engine` is not designed to be instanciated, but to be inherited from.

        It handles basic generic function that allow log gestion, writting, loading json, printing...
        Args:
            None (None): no parameter are required

        Returns:
            bool: The return value. True for success, False otherwise.
        """

    def __init__(self):
        self.reactive_keyword = []
        self.verbose = True
        self.log = []
        self.id = -1
        self.name = "default Engine"
        self.current_folder = dirname(__file__)
        self.dl_directory = os.path.join(dirname(self.current_folder), "dl")
        self.callback = lambda x :None
        print("Engine created")

    def react_to_keyword(self, keyword):
        """ return True if the motor is meant to react to the given url, False else """
        for k in self.reactive_keyword:
            if k in keyword:
                return True
        return False

    def print_v(self, *text):
        # allow to print considering the verbose parameter:
        self.log.append(" ".join(text))
        if self.verbose:
            print(*text)

    def get_logs(self, sep = " \n "):
        logi = ""
        for line in self.log:
            logi+=line + sep
        return logi

    def get_json_file(self, path):
        with open(path, "r", encoding="utf8") as flux:
            data = json.load(flux)
        return data

    def save_json_file(self, data, path):
        with open(path, "w", encoding="utf8") as flux:
            flux.write(json.dumps(data, indent=4))

    def purify_name(self, name, replacement = "_"):
        forbidden_char = ["<", ">","\"", "|", "?", "*", " ", "!", "'" ]
        return "".join(letter if letter not in forbidden_char else replacement for letter in name )

    def make_directory(self, directory):
        """Make a directory if it doesn't exist. The default value is directly in the dl folder
        ARGS:
            directory : path of the to-create directory
        RETURN:
            True if no error
            False else
        """
        try:
            if directory != "": # thus, the directory has been chosen
                if not os.path.exists(directory):
                    os.makedirs(directory)
            else: # wasn't specified, we just recreate the dl path if it doesn't already exists
                if not os.path.exists(self.dl_directory):
                    os.makedirs(self.dl_directory)
                directory = self.dl_directory
                print("directory void, we will save in the ")
            print(directory)
            return directory
        except:
            return False