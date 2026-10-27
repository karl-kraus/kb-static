import os
import unicodedata

HTML_DIR = "src"
HTML_DATA_DIR = os.path.join(HTML_DIR, "data")
LISTBIBL = os.path.join("data", "indices", "listbibl.xml")
LISTPERSON = os.path.join("data", "indices", "listperson.xml")
LISTPLACE = os.path.join("data", "indices", "listplace.xml")


def tokenize(text: str) -> list[str]:
    return "".join(
        " " if unicodedata.category(char).startswith("P") else char for char in text
    ).split()
