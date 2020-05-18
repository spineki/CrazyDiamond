from typing import List, Dict


class Page:
    def __init__(self, number: int, link: str):
        self.number = number
        self.link = link


class Chapter:
    def __init__(self, name ="", link="", number=-1, number_page=-1):
        self.name = name
        self.link = link
        self.number = number
        self.number_page = number_page
        self.manga_name = ""
        self.pages_list = []

    def add_page(self, page: Page) -> None:
        self.pages_list.append(page)

    def add_pages(self, pages_list: List[Page]) -> None:
        for page in pages_list:
            self.pages_list.append(page)


class Volume:
    def __init__(self, name="", link="", number=-1):
        self.name = name
        self.link = link
        self.number = number
        self.chapters_list = []

    def add_chapter(self, chapter: Chapter) -> None:
        self.chapters_list.append(chapter)

    def add_chapters(self, chapters_list: List[Chapter]):
        for chapter in chapters_list:
            self.chapters_list.append(chapter)


class Manga:
    def __init__(self, name="", link="", synopsis=""):
        self.name = name
        self.link = link
        self.synopsis = synopsis
        self.volumes_list = []

    def __str__(self):
        return "manga with name: {0}, link: {1}, synopsis: {2}".format(self.name, self.link, self.synopsis)

    def add_volume(self, volume: Volume) -> None:
        self.volumes_list.append(volume)

    def to_json(self) -> Dict:
        return {"name": self.name, "link": self.link}

    def from_json(self, data: Dict):
        self.name = data["name"]
        self.link = data["link"]

