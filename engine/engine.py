import json
import os

from PIL import Image

class Engine:

    def __init__(self):
        self.reactive_keyword = []
        self.verbose = True
        self.log = []
        self.name = "default Engine"
        self.root_path = os.getcwd()
        self.dl_path = os.getcwd() + "/dl/"
        self.path = os.getcwd() + "/Engine"
        self.callback = lambda x :None
        print(self.path)
        print("Engine created")

    def react_to_keyword(self, keyword):
        """ return True if the motor is meant to react to the given url, False else """
        for k in self.reactive_keyword:
            if k in keyword:
                return True
        return False

    def print_v(self, text):
        # allow to print considering the verbose parameter:
        self.log.append(text)
        if self.verbose:
            print(text)

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
                if not os.path.exists(self.dl_path):
                    os.makedirs(self.dl_path)
                directory = self.dl_path
                print("directory void, we will save in the ")
            print(directory)
            return directory
        except:
            return False