from Engine.EngineManga.engineMangas import EngineMangas
from Engine.EngineManga.scansManga import EngineScansMangas
from Engine.EngineManga.lelScan import EngineLelscan

import time
import pprint
import aiohttp
import asyncio
import aiofiles as aiof
from aiofile import AIOFile, Writer
import aiofiles
from contextlib import closing


""" hgfhksg
Args:

Returns:

Raises:

Example:


 """

# python -m pytest --ignore=envs
# done
# engine
# engineMangas
# scansManga
# pdoc --http : my_package
#

import requests


# You must initialize logging, otherwise you'll not see debug output.

e = EngineLelscan()
# r = e.download_volume_from_manga_name("jojo", 114, "E:\PycharmProject\CrazyDiamond\dl\JoJo_s_Bizarre_Adventure\JoJo_s_Bizarre_Adventure_V114", display_only=False)
pp = pprint.PrettyPrinter(indent=4)

r = e.get_all_available_manga_list()
pp.pprint(r)
r = e.find_manga_by_name("World")
pp.pprint(r)

