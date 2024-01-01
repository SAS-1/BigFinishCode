import json
import os
import shutil
import time
import xml.dom.minidom
import zipfile
from pathlib import Path
import csv

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

json_array = []

for path in Path("JSON").rglob("*.json"):
    print(str(path))

    with open(str(path), "r", encoding="utf-8") as f:
        data = json.load(f)

    data["FileName"] = path.name

    with open("DrWhoAudiobooks.csv", mode="a+", encoding="utf-8", newline="") as file:
        file_writer = csv.writer(
            file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL
        )

        file_writer.writerow(
            [
                data["SeriesTitle"],
                data["ProductTitle"],
                data["ReleaseDate"],
                data["FileName"],
                data["Description"],
            ]
        )
