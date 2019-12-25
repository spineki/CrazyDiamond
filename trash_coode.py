from Engine.EngineManga.engineMangas import EngineMangas
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

def asyncDownload(url_list, url_folder_path):

    async def get(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                print(response.status)
                return None

    async def save(path, content):
        if content == None:
            return None
        try:
            async with aiof.open(path, 'wb') as afp:
                await afp.write(content)
                await afp.flush()
            return True
        except:
            return False


    if len(url_list) != len(url_folder_path):
        return None
    print("after")
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*[get(url) for url in url_list]))

    results = loop.run_until_complete(asyncio.gather(*[save(url_folder_path[i], results[i]) for i in range(len(url_list))]))
    return results

t = time.clock()
asyncDownload(["https://c.japscan.co/lel/Kingdom/625/01.png",
               "https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/107/02.png",
               "https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/107/03.png",
               "https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/107/04.png",
               "https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/107/05.png"],
              ["a.png",
               "b.png",
               "c.png",
               "d.png",
               "e.png"]
              )
print(time.clock() - t , "s")