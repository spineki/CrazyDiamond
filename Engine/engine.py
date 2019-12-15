import json
import os
from os.path import dirname


class Engine:
    """ The super Class `Engine` is not designed to be instanciated, but to be inherited from.
        It handles basic generic function that allow log gestion, writting, loading json, printing...
    """

    def __init__(self):
        self.reactive_keyword = []
        self.verbose = True
        self.log = []
        self.id = -1
        self.name = "default Engine"
        self.current_folder = dirname(__file__)
        self.dl_directory = os.path.join(dirname(self.current_folder), "dl")
        self.callback = lambda x: None
        print("Engine created")

    def react_to_keyword(self, keyword):
        """ Verify if an engine is supposed to react to the given keyword
        Args:
            keyword (string): keyword that will be verified
        Returns:
            bool (bool): True if the keyword is in engine list of reactive keyword, False else
        Raises:
            None (none): None
         """
        for keyword_meant_to_react in self.reactive_keyword:
            if keyword in keyword_meant_to_react:
                return True
        return False

    def print_v(self, *text):
        """ Prints to the terminal the text if self.verbose is True. Keeps in engine logs memory the text

        Args:
            *text (list): texts that can be juxtaposed, or given as a list, and that need to be displayed
        Return:
            None (None):

        Examples:
            >>> e = Engine()
            >>> e.print_v("hi", "I am", "a test")
            >>> ouput: "hi I am a test"
            >>> e.verbose = False
            >>> e.print_v("another test")
            >>> output: None
            >>> e.get_logs()
            >>> ouput: "hi I am a test", "another test"
        """

        self.log.append(" ".join(text))
        if self.verbose:
            print(*text)

    def get_logs(self, sep="\n"):
        """ Gets the logs saved with print_v in a prettified string

        Args:
            sep (string): separator used between each log

        Returns:
            logi (string): prettified logs
        """

        logi = sep.join(self.log)
        return logi

    def get_json_file(self, file_path):
        """ Retrieves json file using json library
        Args:
            file_path (string): Path to the json path with the .json extension.
        Returns:
            data (dict): a json object of the file
            None (None): If there is an error, returns None
        Raises:
            Raises nothing but print_v() the error
        """

        try:
            with open(file_path, "r", encoding="utf8") as flux:
                data = json.load(flux)
            return data
        except Exception as e:
            self.print_v("impossible to load json file ", file_path, " : ", str(e))
            return None

    def save_json_file(self, data, file_path):
        """ Saves json file using json library
        Args:
            data (string): Data that need to be saved in file_path
            file_path (string): Path to the json path with the .json extension.
        Returns:
            bool (bool): True if no error, False else
        Raises:
            Raises nothing but print_v() the error
        """

        try:
            with open(file_path, "w", encoding="utf8") as flux:
                flux.write(json.dumps(data, indent=4))
            return True

        except Exception as e:
            self.print_v("impossible to save in json file ", file_path, " : ", str(e))
            return False

    def purify_name(self, name, replacement="_"):
        """ Purify a string from it's system forbidden characters
        Args:
            name (string): name that need to be purified from forbidden characters
            replacement (string): a replacement character that will replace forbidden chars in name

        Returns:
            string (string): Purified name
            None (None): If there is a mistake

        Raises:
            Raises nothing but print_v() the error
        """

        try:
            forbidden_char = ["<", ">", "\"", "|", "?", "*", " ", "!", "'"]
            return "".join(letter if letter not in forbidden_char else replacement for letter in name)
        except Exception as e:
            self.print_v(" Impossible purify ", name, " : ", str(e))
            return None

    def make_directory(self, directory_path):
        """Make a directory if it doesn't exist.
        Args:
            directory_path : path of the to-create directory
        Returns:
            bool (bool): True if no error, False else

        Raises:
            Raises nothing but print_v() the error
        """
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            return True
        except Exception as e:
            self.print_v("Impossible to create directory ", directory_path, " : ", str(e))
            return False
