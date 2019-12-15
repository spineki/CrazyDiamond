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


e = EngineLelscan()
# e.download_chapter("https://www.lelscan-vf.com/manga/kimetsu-no-yaiba/99")


async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()

async def save(path, content):
    async with aiof.open(path, 'wb') as afp:
        # writer = Writer(afp)
        await afp.write(content)
        await afp.flush()
        #await writer(content)

names = ["01","02","03","04"]

t = time.clock()
loop = asyncio.get_event_loop()
coroutines = [get("https://www.lelscan-vf.com/uploads/manga/kimetsu-no-yaiba/chapters/105/"+ a + ".png") for a in names]
results = loop.run_until_complete(asyncio.gather(*coroutines))
print(time.clock() - t)

# info = results[0].content._buffer[0]
with open("image_async_0.png", "wb") as f:
    f.write(results[0])
with open("image_async_1.png", "wb") as f:
    f.write(results[1])
print("passage aux coroutines")

ref = results[0]

t = time.clock()
coroutines = [save(names[i] + ".png", results[i]) for i in range(len(names))]
results = loop.run_until_complete(asyncio.gather(*coroutines))
print(time.clock() - t)

