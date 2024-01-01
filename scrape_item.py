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

    product_desc = soup.find("div", attrs={"class": "product-desc"})

    series_title = product_desc.find("h6").text.strip()

    product_title = product_desc.find("h3").text.strip()

    release_date = (
        product_desc.find(attrs={"class": "release-date"}).text.strip().split("\t")[-1]
    )

    writers_array = []

    try:
        writers = product_desc.find_all("p")[0]

        for writer in writers.find_all("a"):
            print(f'Writer: {writer["title"]}')
            writers_array.append(writer["title"])
    except:
        print("No writers")

    starring_actors_array = []

    try:
        starring_actors = product_desc.find_all("p")[1]

        for starring_actor in starring_actors.find_all("a"):
            print(f'Starring: {starring_actor["title"]}')
            starring_actors_array.append(starring_actor["title"])
    except:
        print("No starring actors")

    tabs_summary = soup.find(id="tabs")

    about_tab = tabs_summary.find(id="tab1").text.strip()

    cast_tab = tabs_summary.find(id="tab5")

    cast_member_array = []

    try:
        for cast_member in cast_tab.find_all("li"):
            cast_member = (
                cast_member.text.strip()
                .replace("\t", "")
                .replace("\n", " as ")
                .replace("(", "")
                .replace(")", "")
            )

            cast_member_dict = {}
            cast_member_dict["Actor"] = cast_member.split(" as ")[0]
            cast_member_dict["Character"] = cast_member.split(" as ")[-1]

            print(f"Cast member: {cast_member}")
            cast_member_array.append(cast_member_dict)
    except:
        print("No cast members")

    production_credits_tab = tabs_summary.find(id="tab6")

    production_credits_array = []

    for production_credits in production_credits_tab.find_all("li"):
        details = production_credits.text.strip()

        if len(details) > 1:
            details = " & ".join(details.split("\n\t"))

            details = details.replace(" & ", ": ", 1)

        print(details)
        production_credits_array.append(details)

    production_credits_parsed_array = []

    for credit in production_credits_array:
        try:
            credit_role, credit_persons = credit.split(": ", 2)

            for credit_person in credit_persons.split(" & "):
                dict = {}
                dict[credit_role.replace(" by", " By").replace(" ", "")] = credit_person
                production_credits_parsed_array.append(dict)
        except:
            print(f"Encountered issue with text: {credit}")

    # https://www.audiobookshelf.org/docs#book-additional-metadata

    # Details extracted from OPF:
    # title,
    # author,
    # narrator,
    # publishYear,
    # publisher,
    # isbn,
    # description,
    # genres,
    # language,
    # series,
    # volumeNumber

    json_output = {}

    json_output["SeriesTitle"] = series_title
    json_output["ProductTitle"] = product_title
    json_output["ReleaseDate"] = release_date
    json_output["Writers"] = writers_array
    json_output["StarringActors"] = starring_actors_array
    json_output["Description"] = about_tab
    json_output["CastMembers"] = cast_member_array
    json_output["ProductionCredits"] = production_credits_parsed_array

    with open(f"JSON\\{item_url.split('/')[-1]}.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=4)

    opf_fields = {}

    opf_fields["title"] = json_output["ProductTitle"]
    opf_fields["author"] = json_output["Writers"]
    opf_fields["narrator"] = json_output["StarringActors"]
    opf_fields["publishYear"] = json_output["ReleaseDate"].split(" ")[-1]
    opf_fields["publisher"] = "Big Finish"

    for i in json_output["ProductionCredits"]:
        if "DigitalRetailISBN" in i:
            opf_fields["isbn"] = i["DigitalRetailISBN"]

    opf_fields["description"] = json_output["Description"]
    opf_fields["series"] = json_output["SeriesTitle"]

    metadata = {"metadata": opf_fields}

    json_to_xml = xmltodict.unparse(metadata)

    dom = xml.dom.minidom.parseString(json_to_xml)
    pretty_xml_as_string = dom.toprettyxml()

    # write that then to the same file
    with open(f"OPF\\{item_url.split('/')[-1]}.opf", "w", encoding="utf-8") as file:
        file.write(pretty_xml_as_string)

    func_create_abs_json(f"JSON\\{item_url.split('/')[-1]}.json", overwrite_json)

    func_download_thumbnail(f"JSON\\{item_url.split('/')[-1]}.json")
