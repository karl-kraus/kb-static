import copy
from collections import defaultdict

import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import check_for_hash, get_xmlid, make_entity_label
from acdh_xml_pyutils.xml import NSMAP
from utils import listbibl_file, listperson_file, listplace_file

print("adding bibls to person and place entries")
doc = TeiReader(listbibl_file)
bibl_lookup = defaultdict(list)
for x in doc.any_xpath(".//tei:bibl[@xml:id]"):
    for y in x.xpath("./tei:author/@key", namespaces=NSMAP):
        bibl_node = copy.deepcopy(x)
        xml_id = get_xmlid(bibl_node)
        bibl_node.attrib.pop("{http://www.w3.org/XML/1998/namespace}id", None)
        bibl_node.attrib.pop("{http://www.w3.org/XML/1998/namespace}next", None)
        bibl_node.attrib.pop("{http://www.w3.org/XML/1998/namespace}prev", None)
        bibl_node.attrib["corresp"] = f"#{xml_id}"
        bibl_lookup[check_for_hash(y)].append(bibl_node)

doc = TeiReader(listperson_file)

for bad in doc.any_xpath(".//tei:person[@xml:id]/tei:listBibl"):
    bad.getparent().remove(bad)

for x in doc.any_xpath(".//tei:person[@xml:id]"):
    x.attrib["n"] = make_entity_label(x.xpath("./tei:persName", namespaces=NSMAP)[0])[0]
    xml_id = get_xmlid(x)
    bibls = bibl_lookup[xml_id]
    if bibls:
        listbibl_node = ET.SubElement(
            x, "{http://www.tei-c.org/ns/1.0}listBibl", type="written"
        )
        listbibl_node.attrib["n"] = f"{len(bibls)}"
        for y in bibls:
            listbibl_node.append(copy.deepcopy(y))

ET.indent(doc.any_xpath(".")[0], space="   ")
doc.tree_to_file(listperson_file)

print("and now the places")

doc = TeiReader(listbibl_file)
bibl_lookup = defaultdict(list)
for x in doc.any_xpath(".//tei:bibl[@xml:id]"):
    for y in x.xpath("./tei:pubPlace/@key", namespaces=NSMAP):
        bibl_node = copy.deepcopy(x)
        xml_id = get_xmlid(bibl_node)
        bibl_node.attrib.pop("{http://www.w3.org/XML/1998/namespace}id", None)
        bibl_node.attrib.pop("{http://www.w3.org/XML/1998/namespace}next", None)
        bibl_node.attrib.pop("{http://www.w3.org/XML/1998/namespace}prev", None)
        bibl_node.attrib["corresp"] = f"#{xml_id}"
        bibl_lookup[check_for_hash(y)].append(bibl_node)

doc = TeiReader(listplace_file)

for bad in doc.any_xpath(".//tei:place[@xml:id]//tei:listBibl"):
    bad.getparent().remove(bad)

for x in doc.any_xpath(".//tei:place[@xml:id]"):
    x.attrib["n"] = make_entity_label(x.xpath("./tei:placeName", namespaces=NSMAP)[0])[
        0
    ]
    xml_id = get_xmlid(x)
    bibls = bibl_lookup[xml_id]
    if bibls:
        listbibl_node = ET.SubElement(
            x, "{http://www.tei-c.org/ns/1.0}listBibl", type="published_in"
        )
        listbibl_node.attrib["n"] = f"{len(bibls)}"
        for y in bibls:
            listbibl_node.append(copy.deepcopy(y))

ET.indent(doc.any_xpath(".")[0], space="   ")
doc.tree_to_file(listplace_file)
