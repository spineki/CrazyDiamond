from Engine.EngineManga.engineMangas import EngineMangas
from Engine.EngineManga.scansManga import EngineScansMangas
from Engine.EngineManga.lelScan import EngineLelscan
from Engine.EngineManga.scanOP import EngineScanOP
#from Engine.EngineMusic.youtube import EngineYoutube

import time
import aiohttp
import asyncio
import aiofiles as aiof
import aiofiles


""" hgfhksg
Args:

Returns:

Raises:

Example:


 """

# python -m pytest --ignore=envs
# virtualenv --clear envs
# done
# engine
# engineMangas
# scansManga
# pdoc --http : my_package
# pyreverse -o png -A  -f ALL -my -S  -p sortie Engine

import requests


# You must initialize logging, otherwise you'll not see debug output.

# e = EngineScansMangas()
# r = e.download_volume_from_manga_name("jojo", 114, "E:\PycharmProject\CrazyDiamond\dl\JoJo_s_Bizarre_Adventure\JoJo_s_Bizarre_Adventure_V114", display_only=False)
# e.download_volume_from_manga_name("shingeki", 125, display_only=False)

#e.download_manga("https://scan-op.com/manga/kimetsu-no-yaiba", async_mode=True)
# e.download_range_chapters_from_name("jojo",351, 357, "Berserk Tome 40")
#e.download_volume_from_manga_name("shingeki", 128, display_only=False)


# soup.find_all("div", {"class":"chapter_number"})[10].find("a")
engines = [EngineScansMangas(), EngineLelscan(), EngineScanOP()]

for e in engines:
    print(e.find_manga_by_name("creatu"))


# engines[0].download_manga_from_name('https://scans-mangas.com/lecture-en-ligne/dr-stone/')
exit()
def mini_switch(name, num_chapter):
    link_found = False
    link = ""
    title = ""
    for e in engines:
        result_search = e.get_list_volume_from_manga_name(name)['chapter_list']
        for chapter in result_search:
            if chapter["num"] == num_chapter:
                link_found = True
                link = chapter["link"]
                title = chapter["title"]
                break
        if link_found:
            e.download_volume_from_manga_name(name, num_chapter, display_only=False)
            break


mini_switch("shingeki", 128)

# On peut remplacer if a == [] par if not a:


# e.download_volume_from_manga_name("one piece", 965, display_only=False)
