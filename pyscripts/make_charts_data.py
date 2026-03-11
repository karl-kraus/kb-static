import json
import os

from acdh_tei_pyutils.tei import TeiReader
from config import HTML_DATA_DIR, LISTBIBL

output_file = os.path.join(HTML_DATA_DIR, "bibl-per-yer.json")


os.makedirs(HTML_DATA_DIR, exist_ok=True)

doc = TeiReader(LISTBIBL)

data = {}
for x in doc.any_xpath(".//tei:bibl/tei:date/@when"):
    x = x[:4]
    try:
        data[int(x)] += 1
    except KeyError:
        data[int(x)] = 1

data = dict(sorted(data.items(), key=lambda item: item[0]))

payload = {"categories": [x for x in data.keys()], "items": [x for x in data.values()]}

with open(output_file, "w", encoding="utf-8") as fp:
    json.dump(payload, fp, ensure_ascii=False)
