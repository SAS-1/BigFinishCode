import os
import json
import xmltodict
import xml.dom.minidom

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import time

from create_abs_json_function import func_create_abs_json
from get_image_function import func_download_thumbnail


ua = UserAgent(verify_ssl=False)


def scan_item_url(item_url, driver, overwrite_json=False):
    if not os.path.exists("JSON"):
        os.makedirs("JSON")

    if not os.path.exists("OPF"):
        os.makedirs("OPF")

    driver.get(item_url)

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Update the parsing logic based on the new structure
    product_desc = soup.find("div", attrs={"class": "pdp-right"})
    if product_desc is None:
        print("Error: 'pdp-right' div not found.")
        return

    try:
        series_title = product_desc.find("p", attrs={"class": "mt-0 mb-3 last:mb-0 leading-5 text-bf-rich-black-40 text-sm italic"}).text.strip()
        print(f"Series Title: {series_title}")
    except AttributeError:
        print("Error: Series title not found.")
        series_title = "N/A"

    try:
        product_title = product_desc.find("p", attrs={"class": "mt-0 mb-3 last:mb-0 leading-tight text-bf-white-ghost text-md font-bold font-apertura"}).text.strip()
        print(f"Product Title: {product_title}")
    except AttributeError:
        print("Error: Product title not found.")
        product_title = "N/A"

    try:
        release_date_div = product_desc.find("div", attrs={"class": "pdp-released flex items-baseline mb-2"})
        release_date = release_date_div.find_all("p")[1].text.strip()
        print(f"Release Date: {release_date}")
    except (AttributeError, IndexError):
        print("Error: Release date not found.")
        release_date = "N/A"

    # Extract writers, cast, and summary from the new structure
    details_section = soup.find("div", attrs={"class": "pdp-bottom__details px-4 md:px-0 max-w-[736px] ml-auto mr-auto"})

    # Extract summary
    try:
        summary_section = details_section.find("div", attrs={"id": "summary-section"})
        about_tab = summary_section.find("div", attrs={"class": "prose"}).text.strip()
        print(f"Summary: {about_tab}")
    except AttributeError:
        print("Error: Summary not found.")
        about_tab = "N/A"

    # Extract cast members specifically from the "Cast" section
    cast_member_array = []
    narrators_array = []
    try:
        cast_section = details_section.find("div", attrs={"id": "cast"})
        cast_divs = cast_section.find_all("div", attrs={"class": "pdp-cast-section md:flex py-3 border-b-1 border-bf-rich-black-80"})
        for cast_div in cast_divs:
            role = cast_div.find("p", attrs={"class": "font-bold md:w-72 mb-3 md:mb-0"}).text.strip()
            if role == "Cast":
                cast_list = cast_div.find("ul").find_all("li")
                for cast_member in cast_list:
                    actor_tag = cast_member.find("a")
                    actor = actor_tag.text.strip()
                    # Clean up any extra whitespace and parentheses in the cast_member text
                    cleaned_actor = actor.split("(")[0].strip()
                    narrators_array.append(cleaned_actor)

                    character = cast_member.text.replace(actor, "").strip().strip("() ").strip()
                    cast_member_dict = {"Role": role, "Actor": cleaned_actor, "Character": character}
                    print(f"Cast member: {cast_member_dict}")
                    cast_member_array.append(cast_member_dict)
    except AttributeError:
        print("Error: Cast members not found.")


    # Extract production credits
    production_credits_array = []
    try:
        for cast_div in cast_divs:
            role = cast_div.find("p", attrs={"class": "font-bold md:w-72 mb-3 md:mb-0"}).text.strip()
            if role != "Cast":
                credits_list = cast_div.find("ul").find_all("li")
                for credit in credits_list:
                    person = credit.find("a").text.strip()
                    production_credits_array.append({role: person})
                    print(f"Production credit: {role}: {person}")
    except AttributeError:
        print("Error: Production credits not found.")

    # Writers are part of production credits under the role "Writer"
    writers_array = [credit["Writer"] for credit in production_credits_array if "Writer" in credit]

    isbn = ""
    try:
        credits_section = details_section.find("div", attrs={"id": "credits"})
        isbn_p = credits_section.find("p", string=lambda text: text and "Retail ISBN" in text)
        if isbn_p:
            isbn = isbn_p.text.split("Retail ISBN:")[-1].strip()
        print(f"ISBN extracted: {isbn}")
    except AttributeError:
        print("Error: ISBN not found.")

    # The rest of the parsing logic remains unchanged

    json_output = {
        "SeriesTitle": series_title,
        "ProductTitle": product_title,
        "ReleaseDate": release_date,
        "Writers": writers_array,
        "Description": about_tab,
        "CastMembers": cast_member_array,
        "ProductionCredits": production_credits_array,
        "Narrators": narrators_array,
        "ISBN": isbn
    }

    with open(f"JSON\\{item_url.split('/')[-1]}.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=4)

    opf_fields = {
        "title": json_output["ProductTitle"],
        "author": json_output["Writers"],
        "narrator": json_output["Narrators"],
        "publishYear": json_output["ReleaseDate"].split(" ")[-1],
        "publisher": "Big Finish",
        "description": json_output["Description"],
        "series": json_output["SeriesTitle"],
        "isbn": isbn  # Ensure the ISBN is included here
    }

    metadata = {"metadata": opf_fields}

    json_to_xml = xmltodict.unparse(metadata)

    dom = xml.dom.minidom.parseString(json_to_xml)
    pretty_xml_as_string = dom.toprettyxml()

    # write that then to the same file
    with open(f"OPF\\{item_url.split('/')[-1]}.opf", "w", encoding="utf-8") as file:
        file.write(pretty_xml_as_string)

    func_create_abs_json(f"JSON\\{item_url.split('/')[-1]}.json", overwrite_json)

  # commented out as new website doesn't seem to let you download easily
  #   func_download_thumbnail(f"JSON\\{item_url.split('/')[-1]}.json")
