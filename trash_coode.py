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

def asyncDownload(url_list, folder_path_list):

    async def get_and_save(url, path):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    print("un")
                    print(response.status)
                    if response.status == 200:

                        content =  await response.read()
                    else:
                        return False
        except Exception as e:
            # requests error
            return False
        print("deux")
        try:
            async with aiof.open(path, 'wb+') as afp:
                await afp.write(content)
                await afp.flush()
                return True
        except Exception as e:
            print(str(e))
            # saving error
            return False


    if len(url_list) != len(folder_path_list):
        return None
    print("after")
    loop = asyncio.get_event_loop()

    results = loop.run_until_complete(asyncio.gather(*[get_and_save(url_list[i], folder_path_list[i]) for i in range(len(url_list)) ]))
    return results



list_url = ["https://c.japscan.co/lel/Kingdom/625/01.png",
               "https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/107/02.png",
               "https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/107/03.png",
               "https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/107/04.png",
               "https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/107/05.png"]
folder_path_list = ["trash/a.png",
               "trash/b.png",
               "trash/c.png",
               "trash/d.png",
               "trash/e.png"]


print(asyncDownload(list_url, folder_path_list))