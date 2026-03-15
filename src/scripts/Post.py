
from requests import post
from base64 import b64encode

api = "http://localhost:8500"

# Endpoints.
addIMG = f"{api}/orb/addAvatar"
addBG = f"{api}/orb/addbg"
addPOST = f"{api}/orb/NewPostImg"

def MakeMime(fp):
    ext = fp.name.split("/")[-1].split(".")[1]
    print(ext)
    enc = b64encode(fp.read()).decode()
    return f"data:image/{ext};base64,{enc}"

def addAvatar(uuid: int | str, Mime: str) -> dict:
    
    res = post(addIMG, json={
        "uuid": uuid,
        "mime": Mime
    })

    return res.json()

def addbg(uuid: int | str, Mime: str) -> dict:
    res = post(addBG, json={
        "uuid": uuid,
        "mime": Mime
    })

    return res.json()

def addPost(uuid, Mime, post_id=1):
    res = post(addPOST, json={
        "uuid": uuid,
        "mime": Mime,
        "post_id": post_id
    })

    return res.json()


def main():
    path = "./img/img.png"

    with open(path, "rb") as fp:
        print("Opening..")
        uuid = 1
        print("Converting..")
        mime = MakeMime(fp)
        print("Sending..")
        response = addAvatar(uuid, mime)
        if response["code"] == 200:
            print(response["data"]["url"])
        
if __name__ == "__main__":
    main()



