import os
from pathlib import Path
import requests
from fake_useragent import UserAgent
from tqdm import tqdm

ua = UserAgent(verify_ssl=False)

if not os.path.exists("Thumbnails"):
    os.makedirs("Thumbnails")


def func_download_thumbnail(json_filename):
    print(f"Download Thumbnails: {str(json_filename)}")
    json_filename = Path(json_filename)

    big_finish_id = json_filename.stem.split("-")[-1]

    print(big_finish_id)

    image_url = f"https://www.bigfinish.com/image/release/{big_finish_id}/"

    image_filename = os.path.join("Thumbnails", f"{json_filename.stem}.jpg")

    resp = requests.get(
        image_url, stream=True, headers={"User-Agent": ua.chrome}, timeout=30
    )

    total = int(resp.headers.get("content-length", 0))

    if resp.status_code > 200:
        print(f"Error downloading image, status code: {resp.status_code}")
        return

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
