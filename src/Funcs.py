
from os import path
from warnings import catch_warnings

from werkzeug.datastructures.structures import exceptions
from models import Response
from base64 import b64decode
from pathlib import Path
from json import load, dump 
from constants import API_URL, CDN
from random import randint
from hashlib import sha256

assert CDN, "Could not find the cdn, check if it is assigned in the env vars."

TYPES = [
    "img", "bg", "post-"
]

IMG = 0
BG = 1

def makeResponse(code: int = 200, data: dict|str = "No data") -> dict: return Response(code, data).make()

def Save(url: str, ImagePath, Bytes, update = False):
    if path.exists(ImagePath) and not update: return makeResponse(204, "already exists")
    try:
        with open(ImagePath, "wb") as fp: fp.write(Bytes)
    except IOError as _: return makeResponse(500, "Server failed to handle your request")
    return makeResponse(200, {
        "url": url
    })

def Unpack(IMime, TypeIndex: int) -> tuple:
    """ Unpacking the mime image. """
    Extention = IMime.split(";")[0].split(":")[1].split("/")[1]
    Bytes = b64decode(IMime.split(";")[1].split(",")[1].encode())
    FileName = TYPES[TypeIndex]
    if TypeIndex == 2:
        FileName = generateRandomName()

    return Bytes, f"{FileName}.{Extention}"


def SaveUserImage(data: dict, update = False) -> dict:

    MIME, ID = data["mime"], data["id"] 

    if isinstance(ID, int): ID = str(ID)
    Upath = Path(CDN) / ID

    if not Upath.exists(): Upath.mkdir()

    Bytes, FName = Unpack(MIME, IMG)
    ImagePath = Upath / FName
    return Save(f"{API_URL}/Zimg/{ID}/{FName}", ImagePath, Bytes, update)

def getUserImage(uuid: int | str, fname) -> tuple[str, str] | bool:
    if "img" in fname:
        imgPath = Path(CDN) / str(uuid) / fname
        if imgPath.exists():
            Extention = fname.split(".")[1] # get img ext.
            return imgPath, Extention

    return False

def SaveUserBackground(data: dict, update = False) -> dict:
    # TODO: If the calls is comming as a normal post.
    # then it is better to check the update, if it already exists return 400
    MIME, ID = data["mime"], data["id"] 
    if isinstance(ID, int): ID = str(ID)
    Upath = Path(CDN) / ID
    if not Upath.exists(): Upath.mkdir()
    Bytes, FName = Unpack(MIME, BG)
    ImagePath = Upath / FName
    return Save(f"{API_URL}/Zimg/bg/{ID}/{FName}", ImagePath, Bytes, update)
def getUserBg(uuid: str | int, fname) -> tuple[str, str] | bool:
    if "bg" in fname:
        imgPath = Path(CDN) / str(uuid) / fname
        if imgPath.exists():
            Extention = fname.split(".")[1] # get img ext.
            return imgPath, Extention
    return False

def generateRandomName():
    return sha256("".join([chr(i) for i in [randint(0, 100) for i in range(32)]]).encode()).hexdigest()
    

def saveUserPostImage(data: dict) -> dict:
   
    MIME, ID, PID = data["mime"], data["id"], data["postID"]
    
    if not isinstance(MIME, list):
    
        if isinstance(ID, int): ID = str(ID)
        if isinstance(PID, int): PID = str(PID)
        
        Upath = Path(CDN) / ID

        if not Upath.exists(): Upath.mkdir()

        PostsPath = Upath / "posts"

        if not PostsPath.exists(): PostsPath.mkdir()

        currentPostPath = PostsPath / PID

        if not currentPostPath.exists(): currentPostPath.mkdir()

        Bytes, FName = Unpack(MIME, 2)

        ImagePath = currentPostPath / FName
        return Save(f"{API_URL}/Zimg/post/{ID}/{PID}/{FName}", ImagePath, Bytes)

    return makeResponse(400, "Can not save multiple mimes at the moment.")


def GetUserPostImg(uuid: str | int, pid: int | str, fname) -> tuple[str, str] | bool:

    imgPath = Path(CDN) / str(uuid) / "posts" / str(pid) / fname

    if imgPath.exists():
        Extention = fname.split(".")[1] # get img ext.
        return imgPath, Extention
    return False
