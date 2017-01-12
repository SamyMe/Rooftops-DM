#!/usr/bin/env python3
import argparse
import json
import os
import sys
import numpy as np
import matplotlib.pyplot as plt


# get json path
parser = argparse.ArgumentParser()
parser.add_argument('--json', help='Path to the .json')
args = parser.parse_args()
json_path = args.json
if (args.json is None or not os.path.isfile(args.json) or args.json[-5:] != ".json"):
    print("Please provide a valid path to a json listing with '--json'")
    sys.exit(0)

# get the data from the json
json_ads = {}
with open(json_path, 'rt') as f:
    json_ads = json.loads(f.read())
prices = sorted([json_ads[ref]["price"] for ref in json_ads])
bins = np.linspace(prices[0], prices[-1], num=100)

#visualize the data
print("Nb of ads:", len(prices))
print("Max price:", prices[-1])
plt.plot(range(len(prices)), sorted(prices))
plt.show()

print("Bins:", bins)
plt.hist(prices, bins=bins)
plt.show()
