#!/usr/bin/env python3
import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import utils_json as uj
from sklearn.manifold import TSNE


# get json path
parser = argparse.ArgumentParser()
parser.add_argument('--json', help='Path to the .json')
args = parser.parse_args()
json_path = args.json
if (args.json is None or not os.path.isfile(args.json) or args.json[-5:] != ".json"):
    print("Please provide a valid path to a json ads file with '--json'")
    sys.exit(0)

# extraction of prices ands areas
ads_dict = uj.load_json(json_path)
areas, prices = [], []
for ad_ref in ads_dict:
    if ads_dict[ad_ref]["surface"] != '':
        areas.append(float(ads_dict[ad_ref]["surface"].replace(',', '.')))
        prices.append(ads_dict[ad_ref]["price"])

# simple plot and coloration
def get_colors(values):
    median = np.median(values)
    return ["b" if val < median else "r" for val in values]
colors = get_colors(areas)
plt.scatter(areas, prices, c=colors)
plt.show()

# dump
dump_dir = "./data/plots/"
if not os.path.exists(dump_dir):
    os.makedirs(dump_dir)
points_dict = {}
for ad in ads_dict:
    if ads_dict[ad]["surface"] == '':
        continue
    points_dict[ad] = [ads_dict[ad]["price"], float(ads_dict[ad]["surface"].replace(",", "."))]
uj.dump_json(dump_dir + "data_price_per_area.json", points_dict)
