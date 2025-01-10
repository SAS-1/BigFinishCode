import json
import os
import glob
from pathlib import Path

import numpy as np


#search_path = "X:\\Media\\Audiobooks - Doctor Who\\Big Finish Productions\\8. Sherlock Holmes (SH)\\02. Series 02"
search_path = "Z:\\Torrents\\completed\\5. May"

for json_filename in Path(search_path).rglob("*.json"):
    print(str(json_filename))

    new_json_file = os.path.join(str(json_filename.parent), "metadata.json")

    if json_filename.name != "metadata.json":
        if not os.path.exists(new_json_file):
            os.rename(str(json_filename), new_json_file)
        else:
            os.remove(str(json_filename))
