#!/usr/bin/env python3
import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
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

# plots
for f in files:
    print(f)
    emb_json = DATA_DIR + f
    assert os.path.isfile(emb_json)
    ads_json = "data/main/seloger_ads_compressed.json"
    assert os.path.isfile(ads_json)

    emb_dict = uj.load_json(emb_json)
    emb_keys = sorted(list(emb_dict.keys()))
    ads_dict = uj.load_json(ads_json)

    xs = [emb_dict[key][0] for key in emb_keys]
    ys = [emb_dict[key][1] for key in emb_keys]
    prices = [ads_dict[key]["price"] for key in emb_keys]
    areas = [ads_dict[key]["surface"] for key in emb_keys]
    areas = [float(surf.replace(',', '.')) if surf != '' else -1 for surf in areas]

    def get_colors(values):
        p3 = np.percentile(values, 30)
        p6 = np.percentile(values, 70)
        return ["b" if val < p3 else "m" if val < p6 else "r" for val in values]
    colors = get_colors(areas)
    plt.scatter(xs, ys, c=colors, alpha=.15, edgecolors=colors)
    plt.show()
    input()
