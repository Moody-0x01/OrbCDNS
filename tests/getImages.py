#!/usr/bin/env python3

import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://www.newgrounds.com/art"
SAVE_DIR = "./img"
SCROLL_PAUSE = 2

os.makedirs(SAVE_DIR, exist_ok=True)

driver = webdriver.Firefox()
driver.get(URL)

downloaded = set()
# last_height = driver.execute_script("return document.body.scrollHeight")
container = driver.find_element(By.CLASS_NAME, "body-main")

while True:


    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images:
        src = img.get_attribute("src")

        if not src or src in downloaded:
            continue

        try:
            r = requests.get(src, timeout=10)
            name = src.split("/")[-1].split("?")[0]
            if img.get_attribute("title"):
                name = img.get_attribute("title")
            path = os.path.join(SAVE_DIR, name)

            with open(path, "wb") as f:
                f.write(r.content)

            downloaded.add(src)
            print("Downloaded:", name)

        except Exception as e:
            print("Failed:", src)
driver.quit()

