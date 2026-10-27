import os
import unicodedata

HTML_DIR = "src"
HTML_DATA_DIR = os.path.join(HTML_DIR, "data")
LISTBIBL = os.path.join("data", "indices", "listbibl.xml")
LISTPERSON = os.path.join("data", "indices", "listperson.xml")
LISTPLACE = os.path.join("data", "indices", "listplace.xml")


stop_words = [
    "der",
    "die",
    "das",
    "den",
    "dem",
    "des",
    "ein",
    "eine",
    "einer",
    "einen",
    "einem",
    "eines",
    "in",
    "im",
    "ins",
    "an",
    "am",
    "auf",
    "aus",
    "bei",
    "bis",
    "durch",
    "für",
    "gegen",
    "mit",
    "nach",
    "über",
    "um",
    "von",
    "vor",
    "zu",
    "zum",
    "zur",
    "und",
    "oder",
    "aber",
    "als",
    "auch",
    "wie",
    "was",
    "wer",
    "the",
    "a",
    "an",
    "and",
    "as",
    "by",
    "for",
    "from",
    "in",
    "of",
    "on",
    "or",
    "to",
    "with",
    "karl",
    "Kraus",
    "hrsg",
]


def tokenize(text: str, stop_words: list[str] = stop_words) -> list[str]:
    tokens = "".join(
        " " if unicodedata.category(char).startswith("P") else char for char in text
    ).split()
    normalized_stop_words = {word.casefold() for word in stop_words}
    return [token for token in tokens if token.casefold() not in normalized_stop_words]
