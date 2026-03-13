#!/bin/python
from os import scandir
import time
from methods import *

Avatars = [entry.path for entry in scandir('./img/avatars/')]
success = 0
total = len(Avatars)

def test_avatar_store():
    global success, total
    success = 0
    failure = 0
    total = len(Avatars)

    for i, img in enumerate(Avatars):
        with open(img, "rb") as fp:
            uuid = i
            mime = MakeMime(fp)
            print(f"Sending #{i} {img}")
            time.sleep(1)
            response = addAvatar(uuid, mime)
            if response.status_code == 200: success += 1
            else: print(response)

def main():
    test_avatar_store()
    print(f"[ {success} / {total} ]")

if __name__ == "__main__": main()
