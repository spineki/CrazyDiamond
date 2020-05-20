from typing import List, Dict, Tuple


class Page:
    def __init__(self, number: int, link: str):
        self.number = number
        self.link = link

    def __str__(self):
        return "page with number{0}, link{1}".format(self.number, self.link)


class Chapter:
    def __init__(self, name="", link="", number=-1, number_page=-1):
        self.name: str = name
        self.link: str = link
        self.number: int = number
        self.number_page: int = number_page
        self.manga_name: str = ""
        self.pages_list: List[Page] = []

    def __str__(self):
        return "chapter with name:{0}, link:{1}, number:{2}, number of page:{3}, related manga name:{4}"\
            .format(self.name, self.link, self.number, self.number_page, self.manga_name)

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

    def __str__(self):
        return "volume with name:{0}, link:{1}, number:{2}".format(self.name, self.link, self.number)

    def get_min_max_number_chapters(self)-> Tuple[int, int]:
        return min(self.chapters_list, key=lambda x: x.number).number, max(self.chapters_list, key=lambda x: x.number).number

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
        self.volumes_list: List[Volume] = []
        self.chapters_without_volumes_list: List[Chapter] = []

    def __str__(self):
        return "manga with name: {0}, link: {1}, synopsis: {2}".format(self.name, self.link, self.synopsis)

    # GET --------------------------------------------------------------------------------------------------------------
    def get_all_chapters(self) -> List[Chapter]:
        chapters = []
        # adding chapters from volumes
        for volume in self.volumes_list:
            for chapter in volume.chapters_list:
                chapters.append(chapter)

        # adding chapters outside volume
        chapters += self.chapters_without_volumes_list

        return chapters

    # ADD --------------------------------------------------------------------------------------------------------------
    def add_volume(self, volume: Volume) -> None:
        self.volumes_list.append(volume)

    def add_chapters_without_volume(self, chapters_list: List[Chapter]) -> None:
        for chapter in chapters_list:
            self.chapters_without_volumes_list.append(chapter)

    # MORPH ------------------------------------------------------------------------------------------------------------
    def to_json(self) -> Dict:
        return {"name": self.name, "link": self.link}

    def from_json(self, data: Dict):
        self.name = data["name"]
        self.link = data["link"]
