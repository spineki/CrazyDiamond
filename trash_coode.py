from Engine.EngineManga.engineMangas import EngineMangas
from Engine.EngineManga.scansManga import EngineScansMangas
from Engine.EngineManga.lelScan import EngineLelscan
from Engine.EngineManga.scanOP import EngineScanOP
from Engine.EngineManga.mangadex import EngineMangadex
#from Engine.EngineMusic.youtube import EngineYoutube

from typing import List, Optional, Union, Any
from Engine.EngineManga.manga import Manga, Chapter, Volume

import time
import aiohttp
import asyncio
import aiofiles as aiof
import aiofiles


"""e = EngineScanOP()
manga = e.find_manga_by_name("berserk")[0]
print(e.get_manga_info_from_url(manga.link))
print(e.get_all_available_manga_online_list())
print(e.get_info_from_chapter_url("https://scan-op.com/manga/berserk/360"))"""

# scans manga, scan op
# a faire; lelscan



e = EngineMangadex()
mangas = e.find_manga_by_name("jojo")

info = e.get_manga_info_from_name("battle tendency")






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