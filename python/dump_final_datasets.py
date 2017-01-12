#!/usr/bin/env python3
import argparse
import os
import sys
import utils_json as uj



# argparse
parser = argparse.ArgumentParser()
parser.add_argument("--data", help="Path to the data/ directory")
parser.add_argument("--json", help="Path to the .json")
args = parser.parse_args()
DATA_DIR = args.data if args.data[-1] == "/" else args.data + "/"  # "./data/ads/"
if not os.path.exists(DATA_DIR):
    print("Please provide a valid path to the data files with '--data'")
    sys.exit(0)

# filenames
files = ["data_price_per_area.json",
         "data_mds_cityblock.json",
         "data_mds_euclidean.json",
         "data_mds_jaccard.json",
         "data_tsne_cityblock_100.json",
         "data_tsne_cityblock_1000.json",
         "data_tsne_euclidean_100.json",
         "data_tsne_euclidean_1000.json",
         "data_tsne_jaccard_100.json",
         "data_tsne_jaccard_1000.json",]

# dumps
for f in files:
    print(f)
    emb_json = DATA_DIR + f
    assert os.path.isfile(emb_json)
    ads_json = "data/main/seloger_ads_compressed.json"
    assert os.path.isfile(ads_json)

    emb_dict = uj.load_json(emb_json)
    emb_keys = sorted(list(emb_dict.keys()))
    ads_dict = uj.load_json(ads_json)

    out = []
    for key in emb_keys:
        if ads_dict[key]["surface"] == '':
            continue
        ad = {}
        ad["x"] = emb_dict[key][0]
        ad["y"] = emb_dict[key][1]
        ad["price"] = ads_dict[key]["price"]
        ad["area"] = ads_dict[key]["surface"]
        ad["nomagence"] = ads_dict[key]["nomagence"]
        ad["codepostal"] = ads_dict[key]["codepostal"]
        ad["id"] = ads_dict[key]["idannonce"]
        ad["url"] = ads_dict[key]["href"]
        out.append(ad)

    uj.dump_json(DATA_DIR + "final_" + f, out)
