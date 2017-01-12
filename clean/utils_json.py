#!/usr/bin/env python3
import json


def load_json(path):
    with open(path, "rt") as f:
        return json.loads(f.read())

def dump_json(path, d, compact=False):
    with open(path, "wt") as f:
        if not compact:
            f.write(json.dumps(d, indent=4))
        else:
            f.write(json.dumps(d, separators=(',', ':')))
