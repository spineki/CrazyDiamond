from Engine.EngineManga.lelScan import EngineLelscan

def test_get_all_available_manga_list():
    print("pomme")
    e = EngineLelscan()
    manga_list = e.get_all_available_manga_list()
    verif = False
    for manga in manga_list:
        if manga["title"] == 'One Piece':
            verif = True
            break
    assert verif

def test_find_manga_by_name():
    e = EngineLelscan()
    manga = e.find_manga_by_name('Black Butler')
    assert manga == [{'title': 'Black Butler', 'link': 'https://www.lelscan-vf.com/manga/black-butler'}]

def test_get_list_volume_from_manga_url():
    e = EngineLelscan()
    volume_list = e.get_manga_info_from_url("https://www.lelscan-vf.com/manga/hunter-x-hunter")
    assert volume_list["title"] == 'Hunter X Hunter'

def test_get_info_from_chapter_url():
    e = EngineLelscan()
    chapter_info = e.get_info_from_chapter_url("https://www.lelscan-vf.com/manga/the-promised-neverland/157")
    assert chapter_info["max_pages"] == 18


