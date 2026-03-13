import os
import re

from acdh_xml_pyutils.xml import NSMAP
from lxml import etree as ET

listbibl_file = os.path.join("data", "indices", "listbibl.xml")
listperson_file = os.path.join("data", "indices", "listperson.xml")
listplace_file = os.path.join("data", "indices", "listplace.xml")

dummy_entry = """
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="listperson.xml">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title level="a"></title>
                <title level="m">Digitale Karl-Kraus-Bibliographie. Digitalisierte Fassung von Sigurd Paul Scheichls Kommentierter Auswahlbibliographie zu Karl Kraus</title>
                <editor ref="https://d-nb.info/gnd/1036708799">Bernhard Oberreither</editor>
			    <editor ref="https://d-nb.info/gnd/1043833846">Peter Andorfer</editor>
            </titleStmt>
            <publicationStmt>
                <p>Publication Information</p>
            </publicationStmt>
            <sourceDesc>
                <p>Information about the source</p>
            </sourceDesc>
        </fileDesc>
    </teiHeader>
    <text>
        <body>
            <listBibl/>
        </body>
    </text>
</TEI>
"""  # noqa E501


def generate_quote(bibl: ET.Element) -> str:
    """Generate a Chicago-style bibliographic citation from a TEI bibl element."""

    def clean_text(t):
        if not t:
            return ""
        t = t.replace("\n", " ").replace("\r", " ")
        t = re.sub(r"\s+", " ", t)
        return t.strip()

    def join_names(nodes):
        names = [clean_text("".join(n.itertext())) for n in nodes if "".join(n.itertext()).strip()]
        if not names:
            return ""
        if len(names) == 1:
            return names[0]
        if len(names) == 2:
            return f"{names[0]} and {names[1]}"
        return ", ".join(names[:-1]) + ", and " + names[-1]

    authors = join_names(bibl.xpath(".//tei:author", namespaces=NSMAP))
    editors = join_names(bibl.xpath(".//tei:editor", namespaces=NSMAP))

    title_a = bibl.xpath(".//tei:title[@level='a']", namespaces=NSMAP)
    title_m = bibl.xpath(".//tei:title[@level='m'][not(@type='subtitle')]", namespaces=NSMAP)
    subtitle = bibl.xpath(".//tei:title[@level='m'][@type='subtitle']", namespaces=NSMAP)
    title_j = bibl.xpath(".//tei:title[@level='j']", namespaces=NSMAP)
    title_s = bibl.xpath(".//tei:title[@level='s']", namespaces=NSMAP)

    def get(node_list):
        return clean_text("".join(node_list[0].itertext())) if node_list else ""

    title_a = get(title_a)
    title_m = get(title_m)
    subtitle = get(subtitle)
    title_j = get(title_j)
    title_s = get(title_s)

    # Titel + Untertitel immer mit Punkt trennen
    if subtitle:
        title_full = f"{title_m}. {subtitle}"
    else:
        title_full = title_m

    places = [clean_text("".join(p.itertext())) for p in bibl.xpath(".//tei:pubPlace", namespaces=NSMAP)]
    publishers = [clean_text("".join(p.itertext())) for p in bibl.xpath(".//tei:publisher", namespaces=NSMAP)]

    place_str = ", ".join(places)
    publisher_str = ", ".join(publishers)

    date = bibl.xpath(".//tei:date", namespaces=NSMAP)
    year = ""
    if date:
        year = clean_text(date[0].get("when") or (date[0].text or ""))

    scope_nodes = bibl.xpath(".//tei:biblScope", namespaces=NSMAP)
    scope = clean_text(" ".join("".join(s.itertext()) for s in scope_nodes))

    nums = [
        clean_text(n.text)
        for n in bibl.xpath(
            ".//tei:num[not(@type='id') and not(@type='category') and not(@type='series')]",
            namespaces=NSMAP,
        )
        if n.text
    ]
    num = " ".join(nums)

    citation = ""

    # JOURNAL ARTICLE
    if title_a and title_j:

        if authors:
            citation += f"{authors}. "

        citation += f'"{title_a}." {title_j}'

        if num:
            citation += f" {num}"

        if year:
            citation += f" ({year})"

        if scope:
            citation += f": {scope}"

        citation += "."

    # CHAPTER IN EDITED BOOK
    elif title_a and title_m:

        if authors:
            citation += f"{authors}. "

        citation += f'"{title_a}." In: {title_full}.'

        if editors:
            citation += f" Edited by {editors}"

        pub = ""

        if place_str:
            pub += place_str
        if publisher_str:
            pub += f": {publisher_str}" if pub else publisher_str
        if year:
            pub += f" {year}"

        if pub:
            citation += f" {pub}"

        if scope:
            citation += f", {scope}"

        citation += "."

    # MONOGRAPH / EDITED BOOK
    elif title_m:

        if authors:
            citation += f"{authors}. "
        elif editors:
            citation += f"{editors}, ed. "

        citation += f"{title_full}."

        if title_s:
            citation += f" {title_s}."

        pub = ""

        if place_str:
            pub += place_str
        if publisher_str:
            pub += f": {publisher_str}" if pub else publisher_str
        if year:
            pub += f" {year}"

        if pub:
            citation += f" {pub}"

        if scope:
            citation += f", {scope}"

        citation += "."

    citation = re.sub(r"\s+", " ", citation)
    citation = re.sub(r"\.\.+", ".", citation)

    return citation.strip()
    