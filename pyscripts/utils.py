import os
import re

from acdh_xml_pyutils.xml import NSMAP
from lxml import etree as ET

listbibl_file = os.path.join("data", "indices", "listbibl.xml")
listperson_file = os.path.join("data", "indices", "listperson.xml")
listplace_file = os.path.join("data", "indices", "listplace.xml")
listorg_file = os.path.join("data", "indices", "listorg.xml")

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

    # Platzhalter für "und weitere": stehen als eigenes author/editor-Element in den
    # Daten und werden ohne "und" an die Namensliste angehängt.
    others_markers = {"u. a.", "u.a.", "et al.", "et al"}

    def join_names(nodes):
        names = []
        others = ""
        for n in nodes:
            text = clean_text("".join(n.itertext()))
            if not text:
                continue
            if text.lower() in others_markers:
                others = text
                continue
            # Übersetzer kennzeichnen, außer die Daten sagen es schon im Text
            if n.get("role") == "translator" and not text.startswith("Übersetzt"):
                text += " (Übers.)"
            names.append(text)

        if not names:
            return others
        if others:
            return f"{', '.join(names)} {others}"
        if len(names) == 1:
            return names[0]
        return f"{', '.join(names[:-1])} und {names[-1]}"

    # role="translator_monogr": Übersetzer*innen des Sammelwerks/Buches (nicht des
    # Beitrags). Sie stehen nie bei den Autor*innen, sondern nach dem Titel (level m).
    authors = join_names(
        bibl.xpath(".//tei:author[not(@role='translator_monogr')]", namespaces=NSMAP)
    )
    editors = join_names(bibl.xpath(".//tei:editor", namespaces=NSMAP))
    translators_m = join_names(
        bibl.xpath(".//tei:author[@role='translator_monogr']", namespaces=NSMAP)
    )
    if translators_m:
        translators_m = f"Übers. v. {translators_m}."

    title_a = bibl.xpath(".//tei:title[@level='a']", namespaces=NSMAP)
    title_m = bibl.xpath(
        ".//tei:title[@level='m'][not(@type='subtitle')]", namespaces=NSMAP
    )
    subtitle = bibl.xpath(
        ".//tei:title[@level='m'][@type='subtitle']", namespaces=NSMAP
    )
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

    places = [
        clean_text("".join(p.itertext()))
        for p in bibl.xpath(".//tei:pubPlace", namespaces=NSMAP)
    ]
    publishers = [
        clean_text("".join(p.itertext()))
        for p in bibl.xpath(".//tei:publisher", namespaces=NSMAP)
    ]

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
        # Autor*innen des Beitrags (alles außer role="monogr") stehen vorne,
        # Autor*innen des Sammelwerks (role="monogr") nach "In: " vor dem Titel.
        authors_a = join_names(
            bibl.xpath(
                ".//tei:author[not(@role='monogr') and not(@role='translator_monogr')]",
                namespaces=NSMAP,
            )
        )
        authors_m = join_names(
            bibl.xpath(".//tei:author[@role='monogr']", namespaces=NSMAP)
        )

        if authors_a:
            citation += f"{authors_a}. "

        citation += f'"{title_a}." In: '

        if authors_m:
            citation += f"{authors_m}: "

        citation += f"{title_full}."

        if editors:
            citation += f" Hrsg. v. {editors}."

        if translators_m:
            citation += f" {translators_m}"

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
            citation += f"{editors} (Hrsg.). "

        citation += f"{title_full}."

        if translators_m:
            citation += f" {translators_m}"

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
