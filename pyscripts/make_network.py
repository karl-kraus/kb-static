import json
import os

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import (
    any_xpath,
    check_for_hash,
    extract_fulltext,
    get_xmlid,
)
from config import HTML_DATA_DIR, LISTBIBL

os.makedirs(HTML_DATA_DIR, exist_ok=True)
out_file = os.path.join(HTML_DATA_DIR, "network.json")

# shape_example = https://github.com/jacomyal/sigma.js/blob/main/packages/storybook/stories/_data/data.json

graph = {}
nodes = []
edges = []
check_duplicates = ()
years = set()
doc = TeiReader(LISTBIBL)
for x in doc.any_xpath(".//tei:bibl[@xml:id]"):
    bibl_id = get_xmlid(x)
    bibl_label = x.attrib["n"]
    nodes.append({"id": bibl_id, "label": bibl_label, "type": "bibl"})

    # years
    for y in any_xpath(x, "./tei:date[@when]/@when"):
        if y in years:
            pass
        else:
            nodes.append({"id": y, "label": y, "type": "year"})
            edges.append((bibl_id, y))

    # authors:
    for y in any_xpath(x, "./tei:author[@key]"):
        item_id = check_for_hash(y.attrib["key"])
        if item_id not in check_duplicates:
            nodes.append(
                {"id": item_id, "label": extract_fulltext(y), "type": "author"}
            )
            edges.append((bibl_id, item_id))

    # places:
    for y in any_xpath(x, "./tei:pubPlace[@key]"):
        item_id = check_for_hash(y.attrib["key"])
        if item_id not in check_duplicates:
            nodes.append({"id": item_id, "label": extract_fulltext(y), "type": "place"})
            edges.append((bibl_id, item_id))

graph["nodes"] = nodes
graph["edges"] = edges

with open(out_file, "w", encoding="utf-8") as fp:
    json.dump(graph, fp, ensure_ascii=False, indent=2)
