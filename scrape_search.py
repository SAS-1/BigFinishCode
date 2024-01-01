import os
import time
from bs4 import BeautifulSoup

from scrape_item import scan_item_url


def __scroll_down_page(driver, speed=8):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")


def func_scrape_search(driver):
    url_array = []

    driver.get("https://www.bigfinish.com/")

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    for range in soup.find("div", attrs={"class": "submenu-block"}).find_all(
        "a", href=True
    ):
        if range["href"].startswith("/ranges/"):
            url_array.append(range["href"])

            print(range["href"])

    for item_url in url_array:
        print(f"Item URL: {item_url}")

        if "https" not in item_url:
            item_url = f"https://www.bigfinish.com/{item_url}"

        driver.get(item_url)

        time.sleep(3)

        __scroll_down_page(driver)

        print("Completed scrolling")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        page_data = soup.find("div", attrs={"class": "isotope list-area filter2"})

        page_data = page_data.find(id="container")

        link_array = []

        for release in page_data.find_all("li"):
            link = release.find("a", href=True)["href"]

            if link.startswith("/releases/"):
                link_array.append(link)

        num = 0

        for link in link_array:
            num += 1
            print(f"Working on: {link} ({num}/{len(link_array)})")

            if "https" not in link:
                link = f"https://www.bigfinish.com/{link}"

                if os.path.exists(f"JSON\{link.split('/')[-1]}.json"):
                    print(f"Already downloaded: {link.split('/')[-1]}")
                else:
                    print(f"Scanning: {link.split('/')[-1]}")
                    scan_item_url(link, driver)
