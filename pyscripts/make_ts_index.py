import os

import typesense
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import (
    check_for_hash,
    extract_fulltext,
    get_xmlid,
)
from tqdm import tqdm
from typesense.exceptions import ObjectNotFound
from utils import listbibl_file

COLLECTION_NAME = "kb-static"
tag_blacklist = [
    "{http://www.tei-c.org/ns/1.0}abbr",
    "{http://www.tei-c.org/ns/1.0}del",
]
namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}


TYPESENSE_API_KEY = os.environ.get("TYPESENSE_API_KEY", "xyz")
TYPESENSE_TIMEOUT = os.environ.get("TYPESENSE_TIMEOUT", "120")
TYPESENSE_HOST = os.environ.get("TYPESENSE_HOST", "localhost")
TYPESENSE_PORT = os.environ.get("TYPESENSE_PORT", "8108")
TYPESENSE_PROTOCOL = os.environ.get("TYPESENSE_PROTOCOL", "http")
client = typesense.Client(
    {
        "nodes": [
            {
                "host": TYPESENSE_HOST,
                "port": TYPESENSE_PORT,
                "protocol": TYPESENSE_PROTOCOL,
            }
        ],
        "api_key": TYPESENSE_API_KEY,
        "connection_timeout_seconds": int(TYPESENSE_TIMEOUT),
    }
)


try:
    client.collections[COLLECTION_NAME].delete()
except ObjectNotFound:
    pass

current_schema = {
    "name": COLLECTION_NAME,
    "enable_nested_fields": True,
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "rec_id", "type": "string", "sort": True},
        {"name": "title", "type": "string"},
        {"name": "full_text", "type": "string"},
        {"name": ".*_entities", "type": "auto", "facet": True, "optional": True},
    ],
}

client.collections.create(current_schema)

doc = TeiReader(listbibl_file)
records = []
cfts_records = []
for x in tqdm(doc.any_xpath(".//tei:bibl[@xml:id]")):
    xml_id = get_xmlid(x)
    try:
        body = x.xpath("./tei:note[@type='comment']", namespaces=namespaces)[0]
    except IndexError:
        body = "Kein Kommentar"
        print(xml_id)
    record = {}
    record["id"] = xml_id
    record["rec_id"] = xml_id
    record["title"] = x.xpath(".//tei:title[1]", namespaces=namespaces)[0].text
    record["full_text"] = extract_fulltext(x, tag_blacklist=tag_blacklist)

    record["person_entities"] = []
    for y in x.xpath("./tei:author[@key]", namespaces=namespaces):
        item = {}
        item["id"] = check_for_hash(y.attrib["key"])
        item["label"] = y.text
        record["person_entities"].append(item)

    record["place_entities"] = []
    for y in x.xpath("./tei:pubPlace[@key]", namespaces=namespaces):
        item = {}
        item["id"] = check_for_hash(y.attrib["key"])
        item["label"] = y.text
        record["place_entities"].append(item)
    record["category_entities"] = x.xpath(
        "./tei:note[@type='category']", namespaces=namespaces
    )[0].text

    records.append(record)

make_index = client.collections[COLLECTION_NAME].documents.import_(records)
print(make_index)
print("done with indexing")
