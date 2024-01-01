import json
import os
import shutil
import time
import xml.dom.minidom
import zipfile
from pathlib import Path

import requests
import xmltodict
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

ua = UserAgent(verify_ssl=False)

if not os.path.exists("Thumbnails"):
    os.makedirs("Thumbnails")

for path in Path("JSON").rglob("*.json"):
    print(str(path))

    big_finish_id = path.stem.split("-")[-1]

    print(big_finish_id)

    image_url = f"https://www.bigfinish.com/image/release/{big_finish_id}/"

    image_filename = os.path.join("Thumbnails", f"{path.stem}.jpg")

    resp = requests.get(image_url, stream=True, headers={"User-Agent": ua.chrome})

    total = int(resp.headers.get("content-length", 0))

    if resp.status_code > 200:
        print(f"Error downloading image, status code: {resp.status_code}")

        continue

    try:
        with open(image_filename, "wb") as file, tqdm(
            desc=image_filename,
            total=total,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    except Exception as ex:
        print(f"Error downloading file: {image_filename}")
        print("Error:", ex)

        print("Img:", image_url)

        os.remove(image_filename)
