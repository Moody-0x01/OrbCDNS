
from os import environ

CDN = "./storage"
API_URL = "http://localhost:8500"

if "cdn" in environ and environ["cdn"]: CDN = environ["cdn"]
