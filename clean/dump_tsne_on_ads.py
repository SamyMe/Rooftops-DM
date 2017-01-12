#!/usr/bin/env python3
import argparse
import os
import sys
import matplotlib.pyplot as plt
import utils_json as uj
from sklearn.manifold import MDS
from sklearn.manifold import TSNE


# get json path data
parser = argparse.ArgumentParser()
parser.add_argument('--json', help='Path to the .json')
args = parser.parse_args()
emb_json = args.json
if (args.json is None or not os.path.isfile(args.json) or args.json[-5:] != ".json"):
    print("Please provide a valid path to a json word embeddings with '--json'")
    sys.exit(0)

# dump_dir
dump_dir = "./data/plots/"
if not os.path.exists(dump_dir):
    os.makedirs(dump_dir)

# preprocessing
emb_dict = uj.load_json(emb_json)
emb_keys = sorted(list(emb_dict.keys()))
xs, length = [], 50
for i in range(length):
    xs.append(emb_dict[emb_keys[i]])

# tsne
for dist in ["cityblock", "euclidean", "jaccard"]:
    print("====", dist, "====")
    points = TSNE(learning_rate=1000,
                  metric=dist,
                  init="pca",
                  n_iter=2000,
                  random_state=2,
                  verbose=2).fit_transform(xs)
    # points = MDS(metric=dist,
    #              random_state=2,
    #              verbose=2).fit_transform(xs)
    points_dict = {emb_keys[i]: list(points[i]) for i in range(length)}
    uj.dump_json(dump_dir + "data_tsne_" + dist + "_1000.json", points_dict)
    # print(points_dict)
    # plt.scatter(points[:, 0], points[:, 1])
    # plt.show()
