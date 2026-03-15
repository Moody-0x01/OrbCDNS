from socket import gethostbyname, gethostname

from flask import Flask, request, send_file
from models import Response, unwrap_response
from Funcs import (
    SaveUserImage, 
    getUserImage, 
    SaveUserBackground, 
    getUserBg, 
    saveUserPostImage,
    GetUserPostImg,
)

app = Flask(__name__)
PORT = 8500
HOST = gethostbyname(gethostname())
#--------------------------------------------------------------DONEE------------------------------------------------------------------------
@app.route("/orb/addAvatar", methods=["POST"])
def PostUserAvatar(): 
    return unwrap_response(SaveUserImage(request.json))
@app.route("/orb/<uuid>/<fname>", methods=["GET"])
def GetUserAvatar(uuid, fname): return unwrap_response(getUserImage(uuid, fname))
@app.route("/orb/addbg", methods=["POST"])
def PostUserBackground(): return unwrap_response(SaveUserBackground(request.json))
@app.route("/orb/bg/<uuid>/<fname>", methods=["GET"])
def GetUserBackground(uuid, fname): return unwrap_response(getUserBg(uuid, fname))
@app.route("/orb/NewPostImg", methods=["POST"])
def PostUserPostImgs(): return unwrap_response(saveUserPostImage(request.json))
@app.route("/orb/post/<uuid>/<pid>/<fname>", methods=["GET"])
def GetUserPostImgs(uuid, pid, fname): return unwrap_response(GetUserPostImg(uuid, pid, fname))
#--------------------------------------------------------------DONEE------------------------------------------------------------------------
#--------------------------------------------------------------TBD------------------------------------------------------------------------
@app.route("/orb/UpdateUserAvatar", methods=["POST"]) # Not implemented!
def UpdateUserAvatar(): return "Not implemented"
@app.route("/orb/UpdateUserBackground", methods=["POST"]) # Not implemented!
def UpdateUserBackground(): return "Not implemented"
#--------------------------------------------------------------TBD------------------------------------------------------------------------


if __name__ == '__main__':
    # Init the storage dir.
    app.run(host=HOST, port=PORT, debug=True)
