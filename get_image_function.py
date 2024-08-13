import os
from pathlib import Path
import requests
from fake_useragent import UserAgent
from tqdm import tqdm
from bs4 import BeautifulSoup

ua = UserAgent(verify_ssl=False)

if not os.path.exists("Thumbnails"):
    os.makedirs("Thumbnails")

def func_download_thumbnail(json_filename):
    print(f"Download Thumbnails: {str(json_filename)}")
    json_filename = Path(json_filename)

    big_finish_id = json_filename.stem.split("-")[-1]

    print(big_finish_id)

    # URL of the page containing the image
    page_url = f"https://www.bigfinish.com/releases/v/{big_finish_id}"

    try:
        # Fetch the page content
        page_resp = requests.get(page_url, headers={"User-Agent": ua.chrome}, timeout=30)
        page_resp.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page_resp.text, 'html.parser')

        # Find the first image in the image gallery
        image_tag = soup.find("div", class_="glide__slide").find("img")
        image_url = image_tag["src"].strip()

        if not image_url:
            print("Error: Could not find the image URL.")
            return

        # Prepare the filename for the image
        image_filename = os.path.join("Thumbnails", f"{json_filename.stem}.jpg")

        # Download the image
        resp = requests.get(
            image_url, stream=True, headers={"User-Agent": ua.chrome}, timeout=30
        )

        total = int(resp.headers.get("content-length", 0))

        if resp.status_code != 200:
            print(f"Error downloading image, status code: {resp.status_code}")
            return

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

        if os.path.exists(image_filename):
            os.remove(image_filename)

