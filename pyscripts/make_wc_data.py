import json
import os
from collections import Counter

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import any_xpath
from config import HTML_DATA_DIR, LISTBIBL, tokenize

doc = TeiReader(LISTBIBL)

full_title_tokens = []
title_tokens = []
out_file = os.path.join(HTML_DATA_DIR, "wc-title.json")


for x in doc.any_xpath(".//tei:bibl[@n]"):
    full_title = tokenize(x.attrib["n"])
    try:
        title = any_xpath(x, ".//tei:title[@level='a']")[0].text
    except IndexError:
        continue
    title = tokenize(title)
    full_title_tokens.extend(full_title)
    title_tokens.extend(title)

data = {}
title_tokens = Counter([x.lower() for x in title_tokens])
full_title_tokens = Counter([x.lower() for x in full_title_tokens])

data["full_titles"] = [
    {"key": key, "value": value}
    for key, value in full_title_tokens.items()
    if value > 5 and len(key) > 2
]
data["titles"] = [
    {"key": key, "value": value}
    for key, value in title_tokens.items()
    if value > 2 and len(key) > 2
]

with open(out_file, "w", encoding="utf-8") as fp:
    json.dump(data, fp, ensure_ascii=False, indent=2)
