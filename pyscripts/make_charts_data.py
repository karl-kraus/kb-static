import json
import os

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import any_xpath
from config import HTML_DATA_DIR, LISTBIBL, LISTPERSON, LISTPLACE
from utils import listorg_file as LISTORG

os.makedirs(HTML_DATA_DIR, exist_ok=True)

output_file = os.path.join(HTML_DATA_DIR, "bibl-per-year.json")
print(f"generating {output_file}")
doc = TeiReader(LISTBIBL)
data = {}
for x in doc.any_xpath(".//tei:bibl/tei:date/@when"):
    x = x[:4]
    try:
        data[int(x)] += 1
    except KeyError:
        data[int(x)] = 1

data = dict(sorted(data.items(), key=lambda item: item[0]))
payload = {"labels": [x for x in data.keys()], "data": [x for x in data.values()]}
with open(output_file, "w", encoding="utf-8") as fp:
    json.dump(payload, fp, ensure_ascii=False)


output_file = os.path.join(HTML_DATA_DIR, "bibl-per-author.json")
print(f"generating {output_file}")
doc = TeiReader(LISTPERSON)
data = {}
for x in doc.any_xpath(".//tei:person[@xml:id]"):
    label = x.attrib["n"]
    try:
        works_written = int(any_xpath(x, "./tei:listBibl[@n]/@n")[0])
    except IndexError:
        continue
    data[label] = works_written
data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
payload = {"labels": [x for x in data.keys()], "data": [x for x in data.values()]}
with open(output_file, "w", encoding="utf-8") as fp:
    json.dump(payload, fp, ensure_ascii=False)


output_file = os.path.join(HTML_DATA_DIR, "bibl-per-place.json")
print(f"generating {output_file}")
doc = TeiReader(LISTPLACE)
data = {}
for x in doc.any_xpath(".//tei:place[@xml:id]"):
    label = x.attrib["n"]
    try:
        works_written = int(any_xpath(x, "./tei:listBibl[@n]/@n")[0])
    except IndexError:
        continue
    data[label] = works_written
data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
payload = {"labels": [x for x in data.keys()], "data": [x for x in data.values()]}
with open(output_file, "w", encoding="utf-8") as fp:
    json.dump(payload, fp, ensure_ascii=False)


output_file = os.path.join(HTML_DATA_DIR, "bibl-per-org.json")
print(f"generating {output_file}")
doc = TeiReader(LISTORG)
data = {}
for x in doc.any_xpath(".//tei:org[@xml:id]"):
    label = x.attrib["n"]
    try:
        works_written = int(any_xpath(x, "./tei:listBibl[@n]/@n")[0])
    except IndexError:
        continue
    data[label] = works_written
data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
payload = {"labels": [x for x in data.keys()], "data": [x for x in data.values()]}
with open(output_file, "w", encoding="utf-8") as fp:
    json.dump(payload, fp, ensure_ascii=False)


def decade_label(year: int) -> int:
    return (year // 10) * 10


output_file = os.path.join(HTML_DATA_DIR, "authors-decade.json")
min_items = 4
decades = list(range(1900, 2010, 10))
print(decades)
print(f"generating {output_file}")
doc = TeiReader(LISTPERSON)
data = {}
for x in doc.any_xpath(".//tei:person[.//tei:bibl[./tei:date/@when]]"):
    author_label = x.attrib["n"]
    data[author_label] = {}
    for year in any_xpath(x, ".//tei:bibl/tei:date/@when"):
        year = decade_label(int(year[:4]))
        try:
            data[author_label][year] += 1
        except KeyError:
            data[author_label][year] = 1

dataset = []
for author_label, decade_data in data.items():
    if sum(decade_data.values()) < min_items:
        continue
    dataset.append(
        {
            "label": author_label,
            "data": [decade_data.get(decade, 0) for decade in decades],
        }
    )

payload = {"labels": decades, "data": dataset}
with open(output_file, "w", encoding="utf-8") as fp:
    json.dump(payload, fp, ensure_ascii=False)
