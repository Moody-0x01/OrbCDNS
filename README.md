# Orb CDNS

## Notes

- to prevent adding all these config files I just decided to return the url to get the img as a response so it can be accessed from the UI.
- to prevent scrapping I added a func `GenerateRandomID()` for the posts. now you can not just predict the id associated with an image or make a script to get all of them, which is bad..


## TODO

```bash
	
	$ [*] TODO GetUserAvatar(uuid: int) -> imgBytes       
	$ [*] TODO GetUserBackground(uuid: int) -> imgBytes
	$ [*] TODO GetUserPostImgs(uuid: int, postId: int) -> imgBytes[]         
	$ [*] TODO PostUserAvatar(Mime: img, uuid: int) -> result          
	$ [*] TODO PostUserBackground(Mime: img, uuid: int) -> result
	$ [*] TODO PostUserPostImgs(Mimes: img[] | img, uuid, postId: int) -> result
	$ [*] TODO UpdateUserAvatar(uuid: int, NewMime: img) -> imgBytes         
	$ [*] TODO UpdateUserBackground(uuid: int, NewMime: img) -> imgBytes             
	$ [] TODO PostVid(uuid: int, NewMime: video, post_id: int) -> imgBytes             
	$ [] TODO GetPostVid(uuid: int, NewMime: video, post_id: int) -> imgBytes             
	
```
## Tested

```bash
	
	$ [*] TODO GetUserAvatar(uuid: int) -> imgBytes           
	$ [*] TODO GetUserBackground(uuid: int) -> imgBytes          
	$ [*] TODO GetUserPostImgs(uuid: int, postId: int) -> imgBytes[]         
	$ [*] TODO PostUserAvatar(Mime: img, uuid: int) -> result          
	$ [*] TODO PostUserBackground(Mime: img, uuid: int) -> result
	$ [*] TODO UpdateUserAvatar(uuid: int, NewMime: img) -> imgBytes         
	$ [*] TODO UpdateUserBackground(uuid: int, NewMime: img) -> imgBytes             
	$ [*] TODO PostUserPostImgs(Mimes: img[] | img, uuid, postId: int) -> result

```

## Testing

```python

from requests import post
from base64 import b64encode
api = "http://localhost:8500"

# Endpoints.
addIMG = f"{api}/orb/addAvatar"
addBG = f"{api}/orb/addbg"
addPOST = f"{api}/orb/NewPostImg"

def MakeMime(fp): # Makes a mime object to be sent to the server
def addAvatar(uuid: int | str, Mime: str) -> dict: # tries adding an avatar image for a user.
    res = post(addIMG, json={
        "id": uuid,
        "mime": Mime
    })
    return res.json()

def addbg(uuid: int | str, Mime: str) -> dict: # tries adding an background image for a user.
    res = post(addBG, json={
        "id": uuid,
        "mime": Mime
    })

    return res.json()

def addPost(uuid, Mime, postid=1):  # tries adding an post image for a user.
    res = post(addPOST, json={
        "id": uuid,
        "mime": Mime,
        "postID": postid
    })

    return res.json()


def main():
	# Testing the api.*

    path = "./img/img.png"
    success = 0
    total = 2

    with open(path, "rb") as fp:
        uuid = 1
        mime = MakeMime(fp)
        res = addAvatar(uuid, mime)
        if res.code == 200: success+=1
        print(f"{success}/{total}")
        res = addbg(uuid, mime)
        if res.code == 200: success+=1
        print(f"{success}/{total}")
             
if __name__ == "__main__":
    main()

```

## Hierarchy

- This hierarchy is presenting the way the api is saving images.

```bash
    - cdn
	+- <uuid>
	    * img.<Ext>
	    * bg.<Ext>
	    * Config.json
	    	# {"img": "img.jpeg", "bg": "bg.png"} config example
	    +- posts
			+-<postId> if it is more than one image, else: <postId>.<ext>
				* img1.png

```

## routes

NOTE: Will be added when done with the todos above.

- `/orb/addAvatar` add avatar img expects `{"id": some id, "mime": imgMimeObject}`
- `/orb/<uuid>/<fname>` get avatar img expected uuid.
- `/orb/addbg` add background expects `{"id": some id, "mime": imgMimeObject}`
- `/orb/bg/<uuid>/<fname>`	get background expects uuid.
- `/orb/NewPostImg` add user posts with postID, uuid, mime img object.
- `/orb/post/<uuid>/<postID>/<fname>` get a post img using uuid, postID, fname.


## CODES And response examples


- If an certain image was added successfully then the server will response with json. example:

```json
	{
		"code": 200, 
		"data": {
			"url": "http://localhost:8500/orb/bg/1/bg.png"
		}
	}
```

- the response above means that the image is added to the cdn and you can get it using this link `http://localhost:8500/orb/bg/1/bg.png`

- the codes are similar to http codes. you can check em then see if you did actually add the image.

## Why did i make it ?

for fun lol..
and also because I need a cdn for a project m working on. it is a simple social media app.



