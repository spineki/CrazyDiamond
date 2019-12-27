from Engine.EngineManga.engineMangas import EngineMangas
from Engine.EngineManga.scansManga import EngineScansMangas
from Engine.EngineManga.lelScan import EngineLelscan
import time
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

#

import requests


# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.


# You must initialize logging, otherwise you'll not see debug output.

e = EngineScansMangas()
# r = e.download_volume_from_manga_name("jojo", 114, "E:\PycharmProject\CrazyDiamond\dl\JoJo_s_Bizarre_Adventure\JoJo_s_Bizarre_Adventure_V114", display_only=False)

e =EngineMangas()
e.compress_folder("E:\PycharmProject\CrazyDiamond\dl\JoJo_s_Bizarre_Adventure\JoJo_s_Bizarre_Adventure_V105")