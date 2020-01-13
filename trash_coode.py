from Engine.EngineManga.engineMangas import EngineMangas
from Engine.EngineManga.scansManga import EngineScansMangas
from Engine.EngineManga.lelScan import EngineLelscan

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

e = EngineLelscan()
# r = e.download_volume_from_manga_name("jojo", 114, "E:\PycharmProject\CrazyDiamond\dl\JoJo_s_Bizarre_Adventure\JoJo_s_Bizarre_Adventure_V114", display_only=False)
# e.download_volume_from_manga_name("shingeki", 125, display_only=False)

a = []
if not a:
    print("youpi")

# On peut remplacer if a == [] par if not a:

l = ['E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_1.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_2.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_3.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_4.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_5.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_6.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_7.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_8.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_9.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_10.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_11.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_12.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_13.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_14.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_15.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_16.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_17.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_18.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_19.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_20.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_21.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_22.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_23.jpg', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_24.jpg', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_25.jpg', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_26.jpg', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_27.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_28.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_29.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_30.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_31.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_32.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_33.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_34.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_35.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_36.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_37.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_38.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_39.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_40.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_41.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_42.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_43.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_44.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_45.png', 'E:\\PycharmProject\\CrazyDiamond\\dl\\Shingeki_No_Kyojin\\After_Glow_(VA)_V125\\Shingeki_No_Kyojin_125_46.png']

e.download_volume_from_manga_name("one piece", 965, display_only=False)



