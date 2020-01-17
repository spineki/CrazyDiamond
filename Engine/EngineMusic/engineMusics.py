from Engine.engine import Engine
import requests
import bs4

class EngineMusics(Engine):
    """
    The super Class `EngineMusics` is not designed to be instanciated, but to be inherited from.

    It binds every engine that deals with musics.
        The functions defined here performs web and I/O tasks.
    """

    def __init__(self):
        """
        Attributes:
            category (string): category of the Engine; (here, manga).
            Make it easier for the core to sort engines by category.
        """
        super().__init__()
        self.category = "Music"
        self.break_time = 0.1

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
