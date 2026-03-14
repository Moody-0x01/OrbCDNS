#!/usr/bin/env python3
from json import loads
import os
from random import randint
import requests

PAGES=20
HAVEN_KEY = os.environ['WALLHAVEN_API_KEY']
if not HAVEN_KEY:
    print("U can not download wallpapers/backgrounds with no api key please set: WALLHAVEN_API_KEY")
    exit(1)

def generate_seed():
    possible ='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join([possible[randint(0, len(possible))] for _ in range(6)])


def build_query(page, seed, category = "010", purity = "100") -> str:
    """
    page: Which page
    seed: a seed which is 6 letters long to give random results each time.
    category: three bits that represent GENERAL|ANIME|PEOPLE
    purity: three bits that represent SFW|SKETCHY|NSFW
    """
    base = "https://wallhaven.cc/api/v1/search"
    
    return f"{base}?seed={seed}&categories={category}&apikey={HAVEN_KEY}&atleast=1920x1080&page={page}&purity={purity}"

seed = generate_seed()
# print("Seed: ", seed)
final_result = []
for i in range(PAGES):
    query_url = build_query(i+1, seed)
    wallpapers = requests.get(query_url)
    deserialized_list = loads(wallpapers.content)['data']
    # for wall in deserialized_list: final_result.append(wall)
    final_result.append(deserialized_list)

    
# for em in final_result: __import__('pprint').pprint(em)
for em in final_result:
    for img in em:
        # TODO: Get the image and save it at: ./img/backgrounds/
        try:
            u = img['path']
            fn = u.split('/')[-1]
            response = requests.get(img['path'])
            ibytes = response.content
            with open(f"./img/backgrounds/{fn}", "wb+") as fp: fp.write(ibytes)
            print(f"[*] {u} -> {f"./img/backgrounds/{fn}"}")
        except Exception as e:
            raise e
