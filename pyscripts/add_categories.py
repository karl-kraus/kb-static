import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from acdh_xml_pyutils.xml import NSMAP
from utils import generate_quote, listbibl_file

print("adding categories")

doc = TeiReader(listbibl_file)
categories = {}
for x in doc.any_xpath(".//tei:body/tei:desc[@corresp]"):
    for y in x.attrib["corresp"].split():
        categories[f"{y}"] = x.text

for bad in doc.any_xpath(".//tei:note[@type='category']"):
    bad.getparent().remove(bad)

for bad in doc.any_xpath(".//tei:bibl[@xml:id and @n]"):
    del bad.attrib["n"]

for x in doc.any_xpath(".//tei:bibl[@xml:id]"):
    quote = generate_quote(x)
    x.attrib["n"] = quote
    cat_id = x.xpath("./tei:num[@type='category']", namespaces=NSMAP)[0].text
    try:
        cat_text = categories[cat_id]
    except KeyError:
        cat_text = f"Kategorie {cat_id} fehlt"
    cat_node = ET.SubElement(x, "{http://www.tei-c.org/ns/1.0}note", type="category")
    cat_node.text = cat_text
ET.indent(doc.any_xpath(".")[0], space="   ")
doc.tree_to_file(listbibl_file)
