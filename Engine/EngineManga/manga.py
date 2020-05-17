class Manga:
    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.list_volumes = []

    def add_chapter(self, chapter):
        self.list_volumes.append(chapter)
