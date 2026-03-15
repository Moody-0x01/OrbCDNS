
from http import HTTPStatus
from os import environ, mkdir, path
from models import makeResponse
from socket import gethostbyname, gethostname

CDN = "./storage"
host = gethostbyname(gethostname())
API_URL = f"http://{host}:8500"

if "cdn" in environ and environ["cdn"]: CDN = environ["cdn"]
if not path.exists(CDN): mkdir(CDN)
print("CDN storage directory: ", CDN)
TYPES = [
    "img", "bg", "post-"
]

IMG                   = 0
BG                    = 1
MAX_IMAGE_SIZE        = 5 * 1024 * 1024  # 5MB
BadRequest            = makeResponse(HTTPStatus.BAD_REQUEST, "Bad Request! Something is missing or not right")
IncorrectSize         = makeResponse(HTTPStatus.BAD_REQUEST, "Bad Request! Image too big")
Unsupported           = makeResponse(HTTPStatus.BAD_REQUEST, "Bad Request! image data is invalid")
NotFound              = makeResponse(HTTPStatus.NOT_FOUND, "Resource not found")
ServerError           = makeResponse(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal  Server Error")
ResourceAlreadyExists = makeResponse(HTTPStatus.CONFLICT, "resource already exists")
