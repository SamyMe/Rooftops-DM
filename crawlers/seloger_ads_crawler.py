#!/usr/bin/env python3
import argparse
import json
import os
import random as rnd
import requests
import subprocess
import sys
import time
rnd.seed(4)


PROXIES = { 'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050' }
USER_AGENT = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
              + "Chrome/55.0.2883.87 Safari/537.36")
PATH = os.path.dirname(os.path.abspath(__file__)) + "/local_page.html"


# argparse
parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Path to the data/ directory")
parser.add_argument("--json", help="Path to the .json")
args = parser.parse_args()
if (args.json is None or not os.path.isfile(args.json) or args.json[-5:] != ".json"):
    print("Please provide a valid path to a json listing with '--json'")
    sys.exit(0)

DATA_DIR = args.data if args.data[-1] == "/" else args.data + "/" # "./data/ads/"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# json util functions
def load_json(path):
    with open(path, "rt") as f:
        return json.loads(f.read())
def dump_json(path, dict):
    with open(path, "wt") as f:
        f.write(json.dumps(dict, indent=4))

# other util functions
def get_keys_copy(d):
    k = sorted(list(d.keys()))
    rnd.shuffle(k)
    return k
def cur_pos(prst_dict, left_dict):
    prst_len, left_len = len(prst_dict), len(left_dict)
    return str(left_len) + "+" + str(prst_len) + "=" + str(left_len + prst_len)


# get json paths
main_path = args.json
prst_path = main_path[:-5] + "_prst.json"
left_path = main_path[:-5] + "_left.json"

# init the dict and keys
main_dict = load_json(main_path)
main_keys = get_keys_copy(main_dict)
prst_dict = load_json(prst_path) if os.path.isfile(prst_path) else {}
left_dict = {mk: mv for mk, mv in main_dict.items() if mk not in prst_dict}

# make sure that files that are supposed to be present truly are
for ad_ref in prst_dict:
    assert os.path.isfile(DATA_DIR + ad_ref + ".htm")

# make sure the files are consitent with the dicts
dump_json(prst_path, prst_dict)  # if prst_dict == 0 it needs to be created
dump_json(left_path, left_dict)  # left_path should be consitent with main_path and prst_path
assert len(prst_dict) + len(left_dict) == len(main_dict)


# launch the crawl
count = 0
while len(main_dict) > 0:
    # get ad stuff
    ad_ref = main_keys.pop()
    ad_val = main_dict.pop(ad_ref)
    ad_url = ad_val["href"]

    if ad_ref not in prst_dict:
        error = False
        try:
            page = requests.get(ad_url, headers={'user-agent': USER_AGENT}, proxies=PROXIES).text
        except:
            error = True

        if error or "Une erreur s'est produite" in page:
            print(cur_pos(prst_dict, left_dict), "| Skipped")
            subprocess.call(["systemctl", "restart", "tor"])
            time.sleep(1)
        else:
            with open(DATA_DIR + str(ad_ref) + ".htm", "wt") as f:
                f.write(page)
            del left_dict[ad_ref]  # and that is done!
            prst_dict[ad_ref] = ad_val  # add the newly loaded ad to the prst_dict
            print(cur_pos(prst_dict, left_dict), "| Loaded")

        if count % 20 == 0:
            subprocess.call(["systemctl", "restart", "tor"])
            time.sleep(1)

        count += 1
        if count % 10 == 0 or len(main_dict) == 0:
            print("----save----")
            dump_json(prst_path, prst_dict)
            dump_json(left_path, left_dict)
            main_len = len(load_json(main_path))
            prst_len = len(load_json(prst_path))
            left_len = len(load_json(left_path))
            assert dict(load_json(prst_path), **load_json(left_path)) == load_json(main_path)
            # print(load_json(prst_path), "+", load_json(left_path), "=", load_json(main_path))

    if len(main_dict) == 0:  # if the left dict has been scanned entirely
        print("====loop====")
        main_dict = load_json(left_path)  # restart with what's left
        main_keys = get_keys_copy(main_dict)


# ==== NOTES ====
# sudo chown -R user_name ./
