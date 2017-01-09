#!/usr/bin/env python3
import json


def load_json(path):
    with open(path, "rt") as f:
        return json.loads(f.read())

def dump_json(path, dict):
    with open(path, "wt") as f:
        f.write(json.dumps(dict, indent=4))
