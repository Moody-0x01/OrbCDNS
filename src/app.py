from os import mkdir, path
from socket import gethostbyname, gethostname

from flask import Flask, request, send_file

from Funcs import (
    makeResponse, 
    SaveUserImage, 
    getUserImage, 
    SaveUserBackground, 
    getUserBg, 
    saveUserPostImage,
    GetUserPostImg,
    CDN
)

app = Flask(__name__)
PORT = 8500
HOST = gethostbyname(gethostname())

#--------------------------------------------------------------DONEe------------------------------------------------------------------------

@app.route("/orb/addAvatar", methods=["POST"])
def PostUserAvatar():
    data = request.json
    if "id" in data and "mime" in data:
        result = SaveUserImage(data)
        return result

    return makeResponse(400, "could not find id or mime in request form data! please recheck")

@app.route("/orb/<uuid>/<fname>", methods=["GET"])
def GetUserAvatar(uuid, fname):
    
    result = getUserImage(uuid, fname)
    if result:
        file, ext = result
        return send_file(file, mimetype=f'image/{ext}')

    return makeResponse(500, "server could not find config file.")   

@app.route("/orb/addbg", methods=["POST"])
def PostUserBackground():
    data = request.json
    if "id" in data and "mime" in data:
        result = SaveUserBackground(data)
        print(result)
        return result

    return makeResponse(400, "could not find id or mime in request form data! please recheck")

@app.route("/orb/bg/<uuid>/<fname>", methods=["GET"])
def GetUserBackground(uuid, fname):
    
    result = getUserBg(uuid, fname)
    if result:
        file, ext = result
        return send_file(file, mimetype=f'image/{ext}')

    return makeResponse(500, "server could not find config file.")
@app.route("/orb/NewPostImg", methods=["POST"])
def PostUserPostImgs():
    data = request.json

    if "id" in data and "mime" in data and "postID" in data:
        result = saveUserPostImage(data)
        return result

    return makeResponse(400, "could not find id or mime in request form data! please recheck")
@app.route("/orb/post/<uuid>/<postID>/<fname>", methods=["GET"])
def GetUserPostImgs(uuid, postID, fname):
    result = GetUserPostImg(uuid, postID, fname)
    if result:
        file, ext = result
        return send_file(file, mimetype=f'image/{ext}')

    return makeResponse(500, "server could not find config file.")

#--------------------------------------------------------------DONEe------------------------------------------------------------------------

# @app.route("/orb/", methods=["POST"]) # Not implemented!
# def UpdateUserAvatar(): return "Not implemented"
# @app.route("/orb/", methods=["POST"]) # Not implemented!
# def UpdateUserBackground(): return "Not implemented"


if __name__ == '__main__':
    # Init the storage dir.
    if not path.exists(CDN):
        mkdir(CDN)
    app.run(host=HOST, port=PORT, debug=True)
