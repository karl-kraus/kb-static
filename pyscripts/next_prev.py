import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from utils import listbibl_file

print("adding @next and @prev")

doc = TeiReader(listbibl_file)

ids = sorted([x for x in doc.any_xpath(".//tei:bibl[@xml:id]/@xml:id")])
lookup_dict = {}
for i, x in enumerate(ids):
    item = {}
    next_i = i + 1
    prev_i = i - 1
    try:
        item["next"] = ids[next_i]
    except IndexError:
        item["next"] = ids[0]
    item["prev"] = ids[prev_i]
    lookup_dict[x] = item

for x in doc.any_xpath(".//tei:bibl[@xml:id]"):
    xml_id = get_xmlid(x)
    x.attrib["prev"] = lookup_dict[xml_id]["prev"]
    x.attrib["next"] = lookup_dict[xml_id]["next"]

ET.indent(doc.any_xpath(".")[0], space="   ")
doc.tree_to_file(listbibl_file)
