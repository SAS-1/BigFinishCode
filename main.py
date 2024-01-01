import argparse
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from scrape_search import func_scrape_search
from scrape_item import scan_item_url

script_start_time = time.strftime("%Y-%m-%d %H-%M-%S")

options = Options()
# options.add_argument('--headless')
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-gpu")
options.add_argument("--disable-logging")
options.add_argument("--silent")
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument(f"user-data-dir={os.getcwd()}\\selenium")
driver = webdriver.Chrome(
    ChromeDriverManager().install(),
    options=options,
    desired_capabilities=DesiredCapabilities.CHROME,
)


parser = argparse.ArgumentParser(description="Download chapters")
parser.add_argument("-s", "--scan", required=False)
parser.add_argument("-u", "--url", required=False)
parser.add_argument("-o", "--overwrite", required=False, action="store_true")
args = vars(parser.parse_args())

if args["scan"]:
    func_scrape_search(driver)

if args["url"]:
    scan_item_url(args["url"], driver, args["overwrite"])
