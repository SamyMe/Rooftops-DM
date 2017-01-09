#!/usr/bin/env python3
import json


INP_PATH = "crawlers/data_sample/tmp_seloger_ads_indented.json"
with open(INP_PATH, "rt") as f:
    inp_dict = json.loads(f.read())

OUT_PATH = "crawlers/data_sample/tmp_seloger_ads_compressed.json"
with open(OUT_PATH, "wt") as f:
    f.write(json.dumps(inp_dict, separators=(',', ':')))
