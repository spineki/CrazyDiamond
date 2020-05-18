import json
import os
import sys
from os.path import dirname
from typing import List, Union, Any, Optional, Dict


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
        # self.current_folder = dirname(__file__)
        # dealing with bundled application

        if getattr(sys, 'frozen', False):
            self.print_v("frozen mode")
            self.current_folder = os.path.dirname(sys.executable)
            self.dl_directory = os.path.join(self.current_folder, "dl")
        else:
            self.current_folder = os.path.dirname(os.path.abspath(__file__))
            self.dl_directory = os.path.join(dirname(self.current_folder), "dl")

        self.callback = lambda x: None
        self.print_v("Engine created in " + str(self.current_folder))
        self.print_v("dl in " + str(self.dl_directory))

    def react_to_keyword(self, keyword: str) -> bool:
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

    # LOGS ----------------------------------------------------------------------------------------
    def print_v(self, *text: Union[List[Any], str]):
        """ Prints to the terminal the text if self.verbose is True. Keeps in engine logs memory the text
        Args:
            *text (list): texts that can be juxtaposed, or given as a list, and that need to be displayed
        Return:
            None (None):

        Examples:
            >>> e = Engine() # doctest: +ELLIPSIS
            ...
            >>> e.print_v("hi", "I am", "a test")
            hi; I am; a test;
            >>> e.verbose = False

            >>> e.print_v("another test")
            >>> output: None
            >>> e.get_logs()
            "hi I am a test", "another test"
        """

        buffer = ""
        for elem in text:
            buffer += str(elem) + "; "

        self.log.append(buffer)
        if self.verbose:
            print(buffer)

    def get_logs(self, sep="\n"):
        """ Gets the logs saved with print_v in a prettified string

        Args:
            sep (string): separator used between each log

        Returns:
            logi (string): prettified logs
        """

        logi = sep.join(self.log)
        return logi

    # JSON ----------------------------------------------------------------------------------------
    def get_json_file(self, file_path: str) -> Optional[Dict]:
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

    def save_json_file(self, data: Union[List[Any], Dict], file_path: str) -> bool:
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
            with open(file_path, "w+", encoding="utf8") as flux:
                flux.write(json.dumps(data, indent=4))
            return True

        except Exception as e:
            self.print_v("impossible to save in json file ", file_path, " : ", str(e))
            return False

    # DIRECTORY NAME ------------------------------------------------------------------------------
    def purify_name(self, name: str, replacement="_") -> Optional[str]:
        """ Purify a string from its system forbidden characters
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

    def make_directory(self, directory_path: str) -> bool:
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
