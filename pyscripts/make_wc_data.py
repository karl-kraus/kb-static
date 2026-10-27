from collections import Counter

from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import any_xpath
from config import HTML_DATA_DIR, LISTBIBL, tokenize

doc = TeiReader(LISTBIBL)

full_title_tokens = []
title_tokens = []

for x in doc.any_xpath(".//tei:bibl[@n]"):
    full_title = tokenize(x.attrib["n"])
    try:
        title = any_xpath(x, ".//tei:title[@level='a']")[0].text
    except IndexError:
        continue
    title = tokenize(title)
    full_title_tokens.extend(full_title)
    title_tokens.extend(title)

title_tokens = [x.lower() for x in title_tokens]
full_title_tokens = [x.lower() for x in full_title_tokens]
foo = Counter(title_tokens)
print(foo)

print(HTML_DATA_DIR)
