from Engine.EngineMusic.engineMusics import EngineMusics
import os
import youtube_dl
import traceback

class EngineYoutube(EngineMusics):
    """
    A class that parses, searches and downloads musics from youtube
    TODO: add documentation
    """


    def __init__(self):
        super().__init__()
        self.reactive_keyword = ["youtube"]
        self.break_time = 0.1
        self.name = "Youtube"
        self.current_folder = os.path.dirname(__file__)
        self.url_search = "https://www.youtube.com/results?search_query="
        self.url_base = "https://www.youtube.com"

    def find_music_by_name(self, name):

        results = []
        url_search_page = self.url_search + name
        soup = self.get_soup(url_search_page)
        if soup == None:
            return None

        try:
            list_musics_found = soup.find_all("a", {"class":"yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link"})
            for music in list_musics_found:
                try:
                    results.append({"title": music["title"], "link": self.url_base + music["href"]})
                except:
                    pass
        except:
            self.print_v("an error occured while trying to parse the wepage :", url_search_page)
            return None
        return results

    def download_music_from_url(self, url, folder_path=None, format = "ogg"):

        if format == "ogg":
            format = "vorbis"

        if folder_path is None:
            folder_path = self.dl_directory

        try:
            # TODO: possibilité d'ajouter un username et un password!!!
            ydl_opts = {
                'verbose': True,  # like this  # format,vebrose,ottmpl
                'outtmpl': os.path.join(folder_path, "%(title)s.%(ext)s"),  # how can i find
                'format': "bestaudio/best",
                'audioformat': format,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format,
                }],
            }

            ydl = youtube_dl.YoutubeDL(ydl_opts)
            ydl.download([url])

        except Exception as e:
            traceback.print_exc()
            self.print_v("""Impossible to download the musique. Upgrade youtube_dl with 'pip install --upgrade youtube_dl'.
                        If the error is still here, please ask the developper for some help. The error is:""" + str(e))
            return True


