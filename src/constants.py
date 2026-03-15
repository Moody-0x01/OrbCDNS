
from os import environ, mkdir, path
from socket import gethostbyname, gethostname

CDN = "./storage"
host = gethostbyname(gethostname())
API_URL = f"http://{host}:8500"

if "cdn" in environ and environ["cdn"]: CDN = environ["cdn"]
if not path.exists(CDN): mkdir(CDN)
print("CDN storage directory: ", CDN)
