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
    "language": "Eng",
    "explicit": false,
    "abridged": false
}
}
"""


if not os.path.exists("ABS_JSON"):
    os.makedirs("ABS_JSON")

# Define a mapping for series title transformations
series_mapping = {
    "Class": "Class (CL)",
    "Counter-Measures": "Counter Measures (CM)",
    "Cyberman": "Cyberman (CY)",
    "Doctor Who - The Monthly Adventures": "D0. Dr Who - Main Range (MR)",
    "Doctor Who - The First Doctor Adventures": "D1. The First Doctor Adventures (1DA)",
    "Doctor Who - The Tenth Doctor Adventures": "D10. The Tenth Doctor Adventures (10DA)",
    "Doctor Who - The Second Doctor Adventures": "D2. The Second Doctor Adventures (2DA)",
    "Doctor Who - The Third Doctor Adventures": "D3. The Third Doctor Adventures (3DA)",
    "Doctor Who - The Fourth Doctor Adventures": "D4. The Fourth Doctor Adventures (4DA)",
    "Doctor Who - The Fifth Doctor Adventures": "D5. The Fifth Doctor Adventures (5DA)",
    "Doctor Who - The Sixth Doctor Adventures": "D6. The Sixth Doctor Adventures (6DA)",
    "Doctor Who - The Seventh Doctor Adventures": "D7. The Seventh Doctor Adventures (7DA)",
    "Doctor Who - The Eighth Doctor Adventures": "D8. The Eighth Doctor Adventures (8DA)",
    "Doctor Who - The Ninth Doctor Adventures": "D9. The Ninth Doctor Adventures (9DA)",
    "Dalek Empire": "Dalek Empire (DE)",
    "Dark Gallifrey (DG)": "Dark Gallifrey (DG)",
    "Doctor Who - Destiny of the Doctor": "Destiny of the Doctor",
    "Doom's Day": "Doom's Day (DD)",
    "Bernice Summerfield": "F1. Bernice Summerfield (BS)",
    "Bernice Summerfield - Books & Audiobooks": "F2. Bernice Summerfield Audiobooks (BSAB)",
    "Doctor Who - The New Adventures of Bernice Summerfield": "F3. The New Adventures of Bernice Summerfield (NABS)",
    "Gallifrey": "Gallifrey (GAL)",
    "I, Davros": "I, DAVROS",
    "Jago & Litefoot": "Jago & Litefoot (J&L)",
    "Missy": "Missy (MIS)",
    "Doctor Who - Once and Future": "Once and Future (O&F)",
    "Doctor Who - Philip Hinchcliffe Presents": "Philip Hincliffe Presents (PHP)",
    "Doctor Who - Short Trips Rarities": "Rarities & Subcriber Short Trips (SST)",
    "Rose Tyler": "Rose Tyler The Dimension Cannon (RT)",
    "Sarah Jane Smith": "Sarah Jane Smith (SJS)",
    "Doctor Who - Short Trips": "Short Trips (ST)",
    "Doctor Who - Short Trips Rarities": "Short Trips Rarities",
    "The Worlds of Doctor Who - Special Releases": "Special Releases (SP)",
    "Torchwood - Monthly Range": "T0. Torchwood Main Range (TMR)",
    "Torchwood - Special Releases": "T1. Torchwood - Specials (TWsp)",
    "Torchwood One": "T2. Torchwood One (TW1)",
    "Torchwood - The Story Continues": "T3. Torchwood - The Story Continues",
    "Torchwood Soho": "T4. Torchwood Soho (TWS)",
    "Doctor Who - The Audio Novels": "The Audio Novels",
    "Doctor Who - The Companion Chronicles": "The Companion Chronicles (CC)",
    "River Song": "The Diary of River Song (RS)",
    "Doctor Who - The Doctor Chronicles": "The Doctor Chronicles (TDC)",
    "Doctor Who - The Early Adventures": "The Early Adventures (EA)",
    "The Lives of Captain Jack": "The Lives of Captain Jack (LCJ)",
    "Doctor Who - The Lost Stories": "The Lost Stories (LS)",
    "The Paternoster Gang": "The Paternoster Gang (PAT)",
    "The Robots": "The Robots (ROB)",
    "Doctor Who - The Stageplays": "The Stageplays (STG)",
    "Doctor Who - The War Doctor": "The War Doctor (WD)",
    "The War Master": "The War Master (WM)",
    "Doctor Who - Time Lord Victorious": "Time Lord Victorious (TLV)",
    "UNIT": "UNIT (UNIT)",
    "UNIT - The New Series": "UNIT - The New Series (UNITNS)",
    "Iris Wildthyme": "F4. Iris Wildthyme (IW)",
    "Iris Wildthyme and Friends": "F5. Iris Wildthyme & Friends (IWF)",
    "Graceless": "F6. Graceless",
    "Doctor Who - Unbound": "Unbound (UN)",
    "Vienna": "F7. Vienna",
    "Charlotte Pollard": "F9. Charlotte Pollard",
    # Add other series transformations as needed
}

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

#    series_name_and_number = (
#        f"{json_output['SeriesTitle']} #{json_output['ProductTitle'].split('. ')[0]}"
#    )
    # Extract the series number from the product title
    series_number = json_output['ProductTitle'].split('. ')[0]

    # Check if the series title needs to be transformed
    original_series_title = json_output['SeriesTitle']
    modified_series_title = original_series_title

    for key in series_mapping:
        if key in original_series_title:
            modified_series_title = series_mapping[key]
            break

    modified_series_name_and_number = f"{modified_series_title} #{series_number}"

    # Directly use the ISBN from json_output if available
    isbn = json_output.get("ISBN", None)

    abs_metadata_json = {
        "title": json_output["ProductTitle"],
        "subtitle": None,
        "authors": json_output["Writers"],
        "narrators": [actor_info["Actor"] for actor_info in json_output["CastMembers"]],
        "series": [modified_series_name_and_number],
        "genres": ["Audio Drama"],
        "publishedYear": json_output["ReleaseDate"].split(" ")[-1],
        "publishedDate": None,
        "publisher": "Big Finish",
        "description": json_output["Description"].replace("\n", "\n\n"),
        "isbn": isbn,
        "asin": None,
        "language": "Eng",
        "explicit": False,
        "abridged": False
    }

    print("Writing ABS JSON file")
    with open(f"ABS_JSON\\{json_filename.name}", "w", encoding="utf-8") as data_file:
        json.dump(
            {"tags": tags, "chapters": chapters, "metadata": abs_metadata_json},
            data_file,
            indent=4,
        )
