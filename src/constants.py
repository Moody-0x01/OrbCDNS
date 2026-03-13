
from os import environ
from socket import gethostbyname, gethostname

CDN = "./storage"
host = gethostbyname(gethostname())
API_URL = f"http://{host}:8500"

if "cdn" in environ and environ["cdn"]: CDN = environ["cdn"]
