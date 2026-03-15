# TODO: Fix the saves, what if the request is mallformed or the mime is not good????

# from typing import Tuple
from flask import Response as werkzeugResponse, send_file
from os import path
from validation import is_valid_image
from models import makeResponse, Response as genRes
from base64 import b64decode
from pathlib import Path
from constants import API_URL, CDN, IMG, BG, TYPES, MAX_IMAGE_SIZE, BadRequest, IncorrectSize, Unsupported, NotFound, ServerError, ResourceAlreadyExists 

from random import randint
from hashlib import sha256

type Response = werkzeugResponse|genRes

assert CDN, "Could not find the cdn, check if it is assigned in the env vars."

def Save(url: str, ImagePath, Bytes, update = False) -> Response:
    if path.exists(ImagePath) and not update: return ResourceAlreadyExists
    try:
        with open(ImagePath, "wb") as fp: fp.write(Bytes)
    except IOError as _: return ServerError
    return makeResponse(200, { "url": url })

def Unpack(IMime: str, TypeIndex: int) -> tuple:
    """ Unpacking the mime image. """
    Extention = IMime.split(";")[0].split(":")[1].split("/")[1]
    Bytes = b64decode(IMime.split(";")[1].split(",")[1].encode())
    FileName = TYPES[TypeIndex]
    if TypeIndex == 2:
        FileName = generateRandomName()

    return Bytes, f"{FileName}.{Extention}"

def get_mime_info(data: dict, itype: int = IMG) -> Response|tuple[str, bytes, str]:
    if not "mime" in data or "uuid" not in data:
        return BadRequest

    mime, uuid = data["mime"], str(data["uuid"]) if isinstance(data["uuid"], int) else data["uuid"]
    if not isinstance(mime, str):
        return BadRequest

    Upath = Path(CDN) / uuid

    if not Upath.exists():
        Upath.mkdir()

    image_bytes, filename = Unpack(mime, itype)

    if not is_valid_image(image_bytes):
        return Unsupported

    if len(image_bytes) > MAX_IMAGE_SIZE:
        return IncorrectSize
    return uuid, image_bytes, filename

def send_file_object(path: Path) -> Response:
    if path.exists():
        ext = path.name.split(".")[-1]
        return send_file(path, mimetype=f'image/{ext}')
    return NotFound

def SaveUserImage(data: dict, update = False) -> Response:
    info = get_mime_info(data);
    if not isinstance(info, tuple): return info

    uuid, image_bytes, filename = info
    Upath = Path(CDN) / uuid
    ImagePath = Upath / filename
    return Save(f"{API_URL}/orb/{uuid}/{filename}", ImagePath, image_bytes, update)

def getUserImage(uuid: int | str, filename: str) -> Response:
    imgPath = Path(CDN) / str(uuid) / filename
    return send_file_object(imgPath)

def SaveUserBackground(data: dict, update = False) -> Response:
    info = get_mime_info(data, BG);
    if not isinstance(info, tuple): return info
    uuid, image_bytes, filename = info
    Upath = Path(CDN) / uuid
    ImagePath = Upath / filename
    return Save(f"{API_URL}/orb/bg/{uuid}/{filename}", ImagePath, image_bytes, update)

def getUserBg(uuid: str | int, filename: str) -> Response:
    imgPath = Path(CDN) / str(uuid) / filename
    return send_file_object(imgPath)

def generateRandomName() -> str:
    return sha256("".join([chr(i) for i in [randint(0, 100) for i in range(32)]]).encode()).hexdigest()
    

def saveUserPostImage(data: dict) -> Response:
    info = get_mime_info(data, 2);
    if not isinstance(info, tuple): return info
    if not "post_id" in data: return BadRequest
    uuid, image_bytes, filename = info
    pid = str(data["post_id"])
    Upath = Path(CDN) / uuid
    PostsPath = Upath / "posts"
    if not PostsPath.exists():
        PostsPath.mkdir()
    currentPostPath = PostsPath / pid

    if not currentPostPath.exists(): currentPostPath.mkdir()

    ImagePath = currentPostPath / filename
    return Save(f"{API_URL}/orb/post/{uuid}/{pid}/{filename}", ImagePath, image_bytes)

def GetUserPostImg(uuid: str, pid: str, filename: str) -> Response:
    imgPath = Path(CDN) / str(uuid) / "posts" / str(pid) / filename
    return send_file_object(imgPath)
