
from requests import Response, post
from base64 import b64encode
from socket import gethostbyname, gethostname
host = gethostbyname(gethostname())
api = f"http://{host}:8500"

# Endpoints.
addIMG = f"{api}/orb/addAvatar"
addBG = f"{api}/orb/addbg"
addPOST = f"{api}/orb/NewPostImg"

def MakeMime(fp):
    ext = fp.name.split("/")[-1].split(".")[1]
    print(ext)
    enc = b64encode(fp.read()).decode()
    return f"data:image/{ext};base64,{enc}"

def addAvatar(uuid: int | str, Mime: str) -> Response:
    
    res = post(addIMG, json={
        "id": uuid,
        "mime": Mime
    })

    return res

def addbg(uuid: int | str, Mime: str) -> Response:
    res = post(addBG, json={
        "id": uuid,
        "mime": Mime
    })

    return res

def addPost(uuid, Mime, postid=1) -> Response:
    res = post(addPOST, json={
        "id": uuid,
        "mime": Mime,
        "postID": postid
    })

    return res

