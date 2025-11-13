import os
import shutil

import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from utils import dummy_entry, listbibl_file

out_dir = os.path.join("html", "bibl")
shutil.rmtree(out_dir, ignore_errors=True)
os.makedirs(out_dir)
print(f"saving {listbibl_file} into single files {out_dir}")


doc = TeiReader(listbibl_file)
for x in doc.any_xpath(".//tei:bibl[@xml:id]"):
    xml_id = get_xmlid(x)
    save_path = os.path.join(out_dir, f"{xml_id}.xml")
    tei_doc = TeiReader(dummy_entry)
    title = tei_doc.any_xpath(".//tei:titleStmt/tei:title[@level='a']")[0]
    title.text = x.attrib["n"]
    listbibl = tei_doc.any_xpath(".//tei:listBibl")[0]
    listbibl.append(x)
    ET.indent(tei_doc.any_xpath(".")[0], space="   ")
    tei_doc.tree_to_file(save_path)
