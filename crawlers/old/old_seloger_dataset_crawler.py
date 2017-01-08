#!/usr/bin/env python3
import argparse
import json
import os
import requests
import sys


PROXIES = {
    'http': 'socks5://localhost:9050',
    'https': 'socks5://localhost:9050'
}
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64)"
              + "AppleWebKit/537.36 (KHTML, like Gecko)"
              + "Chrome/55.0.2883.87"
              + "Safari/537.36")
JSON_PATH = "seloger_dataset_tmp.json"


# get json path
parser = argparse.ArgumentParser()
parser.add_argument('--path', help='Path to the .json')
args = parser.parse_args()
json_path = args.path

# handle errors
if json_path is None or not os.path.isfile(json_path) or json_path[-5:] != ".json":
    print("Please provide a valid path to a json listing with '--path'")
    sys.exit(0)

# get the data from the json
json_ads = {}
with open(json_path, 'rt') as f:
    json_ads = json.loads(f.read())


for ref in json_ads:
    url = json_ads[ref]["href"]
    print(url)
    break
    page = requests.get(url, headers={'user-agent': USER_AGENT}).text
    with open("local_ad.html", 'w') as f:
        f.write(page)
    print(page)
    break

print(href)


# prices = sorted([json_ads[ref]["price"] for ref in json_ads])
