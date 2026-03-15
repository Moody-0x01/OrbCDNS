#!/bin/python
from os import scandir

from requests import get
from json import loads
from methods import *

Avatars = [entry.path for entry in scandir('./img/avatars/')]
backgrounds = [entry.path for entry in scandir('./img/backgrounds/')]
total = min(10, len(backgrounds))
Avatars = Avatars[:total]
backgrounds = backgrounds[:total]
responses = []

def check_code(response: Response) -> None:
    if response.status_code >= 500:
        print("Server failed to handle this request with: ", response.status_code)
        print("Data sent back: ", response.content)
        exit(1)
    print(f"Url: {response.url} Code: {response.status_code}", end=" ")
    print(f"Content: {response.content[:24]}")

def test_avatar_store():
    for i, img in enumerate(Avatars):
        with open(img, "rb") as fp:
            uuid = i
            mime = MakeMime(fp)
            response = addAvatar(uuid, mime)
            check_code(response)
            if response.status_code == 200:
                responses.append(response)

def _access_check():
    global responses
    for res in responses:
        url = loads(res.content)['url']
        response = get(url)
        check_code(response)
    responses = []

def test_bg_store():
    for  i, background in enumerate(backgrounds):
            uuid = i
            with open(background, "rb") as fp:
                mime = MakeMime(fp)
                response = addbg(uuid, mime)
                check_code(response)
                if response.status_code == 200:
                    responses.append(response)
def main():
    test_avatar_store()
    _access_check()
    test_bg_store()
    _access_check()

if __name__ == "__main__": main()
