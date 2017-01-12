#!/usr/bin/env python3
import argparse
import json
import os
import random as rnd
import sys
from bs4 import BeautifulSoup
from pprint import pprint
import utils_json as uj
rnd.seed(2)


# argparse
parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Path to the data/ directory")
parser.add_argument("--json", help="Path to the .json")
args = parser.parse_args()

# htm paths
DATA_DIR = args.data if args.data[-1] == "/" else args.data + "/"  # "./data/ads/"
if not os.path.exists(DATA_DIR):
    print("Please provide a valid path to the htm files with '--data'")
    sys.exit(0)

# json paths
inp_path, out_path = args.json, args.json[:-5] + "_out" + ".json"
if (inp_path is None or not os.path.isfile(inp_path) or inp_path[-5:] != ".json"):
    print("Please provide a valid path to a json listing with '--json'")
    sys.exit(0)

# launch the parsing
inp_dict = uj.load_json(inp_path)
out_dict = uj.load_json(out_path) if os.path.isfile(out_path) else {}
inp_keys = sorted(list(inp_dict.keys()))
rnd.shuffle(inp_keys)
for i in range(len(inp_dict)):  # the 3rd ad is expired
    # get ad stuff
    inp_ad_ref = inp_keys.pop()
    inp_ad_val = inp_dict.pop(inp_ad_ref)
    htm_path = DATA_DIR + inp_ad_ref + ".htm"

    if inp_ad_ref in out_dict:
        print(str(len(inp_dict)) + " | Ref:" + str(inp_ad_ref)+ " | DONE!")
        continue

    # prepare soup
    with open(htm_path, "rt") as f:
        page = f.read()
    soup = BeautifulSoup(page, 'html.parser')

    # checks
    if not os.path.isfile(htm_path):
        print(str(len(inp_dict)) + " | Skipped (file does not exist)")
        continue
    elif "bellesdemeures.com" in inp_ad_val["href"]:
        print(str(len(inp_dict)) + " | Skipped (bellesdemeures.com)")
        continue
    elif len(soup.find_all("div", {"class": ["title_nbresult"]})) != 0:
        print(str(len(inp_dict)) + " | Skipped (expired ad)")
        continue
    else:
        print(str(len(inp_dict)) + " | Ref:" + str(inp_ad_ref))

    # prepare subsoups
    form_tags = soup.find_all("form", {"class": ["form-contact"]})
    if len(form_tags) < 2:
        print(str(len(inp_dict)) + " | Skipped (form is not right)")
        continue
    assert form_tags[0] == form_tags[1]  # for some reason there are 2 identical forms
    formsoup = form_tags[0]
    ol_tags = soup.find_all("ol", {"class": ["description-liste"]})
    assert len(ol_tags) == 1  # there should be one and only one of those tags
    ol_soup = ol_tags[0]

    # util function and a lot of asserts
    def get_value_from_input_name(name):
        tags = formsoup.find_all("input", {"name": [name]})
        assert len(tags) == 1  # there should be one and only one of those tags
        return tags[0]["value"]
    assert get_value_from_input_name("nomville") == get_value_from_input_name("ville")  # paris
    if get_value_from_input_name("typebien") != "Appartement":
        print(str(len(inp_dict)) + " | Skipped (not an appartment)")
        continue
    assert get_value_from_input_name("typebien") == "Appartement"  # should be an appartment
    assert get_value_from_input_name("naturebien") == "1"  # should be an appartment
    assert get_value_from_input_name("idtt") == "1"  # should be for renting
    assert get_value_from_input_name("idannonce") == inp_ad_ref
    ad_price = int(float(get_value_from_input_name("prix").replace("\xa0", "").replace(",", ".")))
    if ad_price != inp_ad_val["price"] and ad_price + 1 != inp_ad_val["price"]:
        print(len(inp_dict), " | Skipped (!= prices:", ad_price, " vs ", inp_ad_val["price"], ")")
        continue
    assert ad_price == inp_ad_val["price"] or ad_price + 1 == inp_ad_val["price"]

    # start creating the ad dict
    out_ad_val = {}
    out_ad_val["data-publication-id"] = inp_ad_val["data-publication-id"]
    out_ad_val["title"] = inp_ad_val["title"]
    out_ad_val["href"] = inp_ad_val["href"]
    out_ad_val["price"] = inp_ad_val["price"]
    out_ad_val["idannonce"] = get_value_from_input_name("idannonce")
    out_ad_val["idpublication"] = get_value_from_input_name("idpublication")
    out_ad_val["provenance"] = get_value_from_input_name("provenance")
    out_ad_val["source"] = get_value_from_input_name("source")
    out_ad_val["nomagence"] = get_value_from_input_name("nomagence")
    out_ad_val["surface"] = get_value_from_input_name("surface")
    out_ad_val["description"] = get_value_from_input_name("description")
    out_ad_val["codepostal"] = get_value_from_input_name("codepostal")

    # get the true ref
    ref_tags = soup.find_all("span", {"class": ["description_ref"]})
    assert len(ref_tags) == 1 and len(ref_tags[0].contents) == 1
    ref_str = ref_tags[0].contents[0].lstrip().rstrip()
    if ref_str[:7] != 'Réf.:  ':
        print(str(len(inp_dict)) + " | Skipped (Ref is not right)")
        continue
    assert ref_str[:7] == 'Réf.:  '
    out_ad_val["ref"] = ref_str[7:].lstrip().rstrip()

    # get all the tags from the ol "description_liste"
    ad_tags = []
    for li_tag in ol_soup.find_all("li"):
        if li_tag.has_attr("title"):
            ad_tags.append(li_tag["title"].replace("\xa0", "").lstrip().rstrip())
    out_ad_val["tags"] = ad_tags
    out_dict[inp_ad_ref] = out_ad_val
    # pprint(out_ad_val)

    if i % 100 == 0 or len(inp_dict) == 0:  # does not work if last one was skipped
        print("----save----")
        uj.dump_json(out_path, out_dict)
        # print(uj.load_json(out_path))

print("----save----")
uj.dump_json(out_path, out_dict)

# script -c 'python3 ./crawlers/seloger_ads_parser.py --data "./crawlers/data/ads/" --json "./crawlers/03_seloger_listing.json"' parsing_info.txt
