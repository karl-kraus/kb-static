import glob
from collections import defaultdict
from pathlib import Path

from acdh_tei_pyutils.tei import TeiReader
from lxml import etree

files = glob.glob("./data/*/*.xml")

print(len(files))
XML_NS = "{http://www.w3.org/XML/1998/namespace}"


def _letter_suffix(index: int) -> str:
    suffix = ""
    while index >= 0:
        suffix = chr(ord("a") + index % 26) + suffix
        index = index // 26 - 1
    return suffix


def fix_duplicate_xml_ids(xml_file: Path) -> None:
    parser = etree.XMLParser(collect_ids=False)
    tree = etree.parse(str(xml_file), parser)
    ids = defaultdict(list)

    for element in tree.iter():
        xml_id = element.get(f"{XML_NS}id")
        if xml_id:
            ids[xml_id].append(element)

    duplicates = {
        xml_id: elements for xml_id, elements in ids.items() if len(elements) > 1
    }

    if not duplicates:
        return

    used_ids = set(ids)
    seen_ids = set()
    for element in tree.iter():
        xml_id = element.get(f"{XML_NS}id")
        if not xml_id:
            continue
        if xml_id not in seen_ids:
            seen_ids.add(xml_id)
            continue

        suffix_index = 0
        while True:
            new_id = f"{xml_id}{_letter_suffix(suffix_index)}"
            suffix_index += 1
            if new_id not in used_ids:
                break

        element.set(f"{XML_NS}id", new_id)
        used_ids.add(new_id)
        print(
            f"{xml_file}:{element.sourceline}: "
            f"{xml_id} -> {new_id} ({tree.getpath(element)})"
        )

    tree.write(str(xml_file), encoding="UTF-8", xml_declaration=True)


for x in files:
    try:
        doc = TeiReader(x)
    except Exception as e:
        print(x, e)
    fix_duplicate_xml_ids(Path(x))
