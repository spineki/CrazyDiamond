from Engine.EngineManga.engineMangas import EngineMangas
from Engine.EngineManga.scansManga import EngineScansMangas
from Engine.EngineManga.lelScan import EngineLelscan
from Engine.EngineMusic.youtube import EngineYoutube

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

e = EngineYoutube()
# r = e.download_volume_from_manga_name("jojo", 114, "E:\PycharmProject\CrazyDiamond\dl\JoJo_s_Bizarre_Adventure\JoJo_s_Bizarre_Adventure_V114", display_only=False)
# e.download_volume_from_manga_name("shingeki", 125, display_only=False)
e.download_music_from_url("https://www.youtube.com/watch?v=isZhOCyajFI")


# soup.find_all("div", {"class":"chapter_number"})[10].find("a")


# On peut remplacer if a == [] par if not a:


# e.download_volume_from_manga_name("one piece", 965, display_only=False)
