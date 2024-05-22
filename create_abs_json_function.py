import json
import os
import glob
from pathlib import Path

import numpy as np

"""
{
"tags": [],
"chapters": [],
"metadata": {
    "title": "MR 001 - The Sirens of Time",
    "subtitle": null,
    "authors": [
    "1. The Classic Series"
    ],
    "narrators": [],
    "series": [
    "1. Main Range (MR) #1"
    ],
    "genres": [
    "Audio Drama"
    ],
    "publishedYear": "1999",
    "publishedDate": null,
    "publisher": null,
    "description": "New description\n\nfdkgjdfkgljgdflkj",
    "isbn": null,
    "asin": null,
    "language": null,
    "explicit": false,
    "abridged": false
}
}
"""


if not os.path.exists("ABS_JSON"):
    os.makedirs("ABS_JSON")


# for json_filename in Path("JSON").rglob("*.json"):
def func_create_abs_json(json_filename, overwrite_json=False):
    print(f"ABS JSON: {str(json_filename)}")

    json_filename = Path(json_filename)

    if os.path.exists(json_filename):
        with open(json_filename, "r", encoding="utf-8") as f:
            json_output = json.loads(f.read())
    else:
        with open(f"JSON\\{json_filename}", "r", encoding="utf-8") as f:
            json_output = json.loads(f.read())

    if os.path.exists(f"ABS_JSON\\{json_filename.name}") and overwrite_json is False:
        print("ABS JSON exists, skipping")
        return

    tags = []
    chapters = []

    series_name_and_number = (
        f"{json_output['SeriesTitle']} #{json_output['ProductTitle'].split('. ')[0]}"
    )

    isbn = None

    for i in json_output["ProductionCredits"]:
        if "DigitalRetailISBN" in i:
            isbn = i["DigitalRetailISBN"]

    abs_metadata_json = {}

    abs_metadata_json["title"] = json_output["ProductTitle"]
    abs_metadata_json["subtitle"] = None
    abs_metadata_json["authors"] = json_output["Writers"]
    abs_metadata_json["narrators"] = [actor_info["Actor"] for actor_info in json_output["CastMembers"]]
    abs_metadata_json["series"] = [series_name_and_number]
    abs_metadata_json["genres"] = ["Audio Drama"]
    abs_metadata_json["publishedYear"] = json_output["ReleaseDate"].split(" ")[-1]
    abs_metadata_json["publishedDate"] = None
    abs_metadata_json["publisher"] = "Big Finish"
    abs_metadata_json["description"] = json_output["Description"].replace("\n", "\n\n")
    abs_metadata_json["isbn"] = isbn
    abs_metadata_json["asin"] = None
    abs_metadata_json["language"] = "Eng"
    abs_metadata_json["explicit"] = False
    abs_metadata_json["abridged"] = False

    print("Writing ABS JSON file")
    with open(f"ABS_JSON\\{json_filename.name}", "w", encoding="utf-8") as data_file:
        json.dump(
            {"tags": tags, "chapters": chapters, "metadata": abs_metadata_json},
            data_file,
            indent=4,
        )


# func_create_abs_json(
#    "JSON\\doctor-who-the-first-doctor-adventures-volume-01-1692.json",
#    "X:\\Media\\Audiobooks - Doctor Who\\Big Finish Productions\\1. Doctor Who\\1. The Classic Series\\2. The First Doctor Adventures (1DA)\\1. Volume 1",
# )
