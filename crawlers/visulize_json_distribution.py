#!/usr/bin/env python3
import json
import os
import numpy as np
import matplotlib.pyplot as plt


# if there is no json simply return
json_path = "seloger_listing_tmp.json"
if not os.path.isfile(json_path):
    import sys
    print("The file '" + json_path + "' does not exist!")
    sys.exit(0)

# get the data from the json
json_ads = {}
with open(json_path, 'rt') as f:
    json_ads = json.loads(f.read())
prices = sorted([json_ads[ref]["price"] for ref in json_ads])
bins = np.linspace(prices[0], prices[-1], num=20)

#visualize the data
print("Nb of ads:", len(prices))
print("Max price:", prices[-1])
plt.plot(range(len(prices)), sorted(prices))
plt.show()

print("Bins:", bins)
plt.hist(prices, bins=bins)
plt.show()
