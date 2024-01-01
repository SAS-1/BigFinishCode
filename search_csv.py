import json
import os
import shutil
import time
import xml.dom.minidom
import zipfile
from pathlib import Path
import csv
import pandas as pd

import requests
import xmltodict
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from create_abs_json import func_create_abs_json

ua = UserAgent(verify_ssl=False)


def search_csv(search_term):
    df = pd.read_csv(
        "DrWhoAudiobooks.csv",
        sep=",",
        names=["SeriesTitle", "ProductTitle", "ReleaseDate", "FileName"],
    )

    search_result = df.loc[df["ProductTitle"] == search_term]

    return search_result


def search_csv_reader(search_term):
    with open("DrWhoAudiobooks.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            if search_term.upper() in row[1].upper():
                print(row)

                return row


search_path = "X:\\Media\\CompletedTorrents\\8. August"

for path in Path(search_path).rglob("*.mp3"):
    print(str(path))

    if os.path.exists(os.path.join(str(path.parent), "metadata.json")):
        continue

    # trying to get the series code from parent folder, e.g. 1. Main Range (MR) = MR
    series_code = path.parent.parent.name.split("(")[-1].split(")")[0]

    # start by stripping that code out
    # Currently: MR 001 - The Sirens of Time.mp3
    episode_title = path.stem.replace(f"{series_code} ", "")

    # titles will normally be something like: 001. Doctor Who: The Sirens of Time
    episode_title = episode_title.replace(" - ", ". Doctor Who: ")

    print(episode_title)

    result = search_csv(episode_title)

    if not result.empty:
        SeriesTitle, ProductTitle, ReleaseDate, JSONFileName = result.values[0]
        print(f"Series: {SeriesTitle}, Title: {ProductTitle}")

        # func_create_abs_json(JSONFileName, str(path.parent))

        continue

    episode_title = path.stem.split(" - ")[-1]

    result = search_csv_reader(episode_title)

    if result:
        SeriesTitle, ProductTitle, ReleaseDate, JSONFileName = result
        print(f"Series: {SeriesTitle}, Title: {ProductTitle}")

        func_create_abs_json(JSONFileName, str(path.parent))

        continue
