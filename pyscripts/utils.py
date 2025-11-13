import os

from acdh_xml_pyutils.xml import NSMAP
from lxml import etree as ET

listbibl_file = os.path.join("data", "indices", "listbibl.xml")

dummy_entry = """
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="listperson.xml">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title level="a"></title>
                <title level="s">Eine Karl Kraus Bibliographie, basierend auf S.P. Scheichls "Kommentierte Auswahlbibliographie" (KAB)</title>
                <editor ref="https://d-nb.info/gnd/1036708799">Bernhard Oberreither</editor>
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


# this function was written by Claude Sonnet 4.5 because no sane person would do this
def generate_quote(bibl: ET.Element) -> str:
    """Generate a full bibliographic citation from a TEI bibl element.

    Args:
        bibl (ET.Element): a tei:bibl node

    Returns:
        str: A full bibliographic citation in standard bibliographic format
    """
    parts = []

    # Authors/Editors
    authors = bibl.xpath(".//tei:author", namespaces=NSMAP)
    editors = bibl.xpath(".//tei:editor", namespaces=NSMAP)

    if authors:
        author_names = [author.text.strip() for author in authors if author.text]
        if len(author_names) > 1:
            parts.append("; ".join(author_names))
        elif author_names:
            parts.append(author_names[0])
    elif editors:
        editor_names = [editor.text.strip() for editor in editors if editor.text]
        if editor_names:
            parts.append("; ".join(editor_names))

    # Title
    title_m = bibl.xpath(".//tei:title[@level='m']", namespaces=NSMAP)
    title_a = bibl.xpath(".//tei:title[@level='a']", namespaces=NSMAP)
    title_j = bibl.xpath(".//tei:title[@level='j']", namespaces=NSMAP)
    title_s = bibl.xpath(".//tei:title[@level='s']", namespaces=NSMAP)

    # Article title (level='a')
    if title_a:
        title_text = "".join(title_a[0].itertext()).strip()
        parts.append(f'"{title_text}"')

    # Monograph title (level='m')
    if title_m:
        for tm in title_m:
            if tm.get("type") != "subtitle":
                title_text = "".join(tm.itertext()).strip()
                parts.append(title_text)
                break

        # Add subtitle if exists
        subtitle = bibl.xpath(
            ".//tei:title[@level='m'][@type='subtitle']", namespaces=NSMAP
        )
        if subtitle:
            subtitle_text = "".join(subtitle[0].itertext()).strip()
            parts.append(subtitle_text)

    # Journal title (level='j')
    if title_j:
        journal_text = "".join(title_j[0].itertext()).strip()
        parts.append(f"In: {journal_text}")

    # Edition
    edition = bibl.xpath(".//tei:edition", namespaces=NSMAP)
    if edition and edition[0].text:
        parts.append(edition[0].text.strip())

    # Publication place and publisher
    pub_place = bibl.xpath(".//tei:pubPlace", namespaces=NSMAP)
    publisher = bibl.xpath(".//tei:publisher", namespaces=NSMAP)

    pub_info = []
    if pub_place and pub_place[0].text:
        pub_info.append(pub_place[0].text.strip())
    if publisher and publisher[0].text:
        pub_info.append(publisher[0].text.strip())

    if pub_info:
        parts.append(": ".join(pub_info))

    # Series (level='s')
    if title_s:
        series_text = "".join(title_s[0].itertext()).strip()
        series_num = bibl.xpath(".//tei:num[@type='series']", namespaces=NSMAP)
        if series_num and series_num[0].text:
            parts.append(f"({series_text} {series_num[0].text.strip()})")
        else:
            parts.append(f"({series_text})")

    # Date
    date = bibl.xpath(".//tei:date", namespaces=NSMAP)
    if date:
        date_text = date[0].text.strip() if date[0].text else date[0].get("when", "")
        if date_text:
            parts.append(date_text)

    # Issue/volume numbers (for journals)
    nums = bibl.xpath(
        ".//tei:num[not(@type='id') and not(@type='category') and not(@type='series')]",
        namespaces=NSMAP,
    )
    for num in nums:
        if num.text:
            parts.append(num.text.strip())

    # Page range/scope
    bibl_scope = bibl.xpath(".//tei:biblScope", namespaces=NSMAP)
    if bibl_scope:
        for scope in bibl_scope:
            scope_text = "".join(scope.itertext()).strip()
            if scope_text:
                parts.append(scope_text)

    # Join all parts with appropriate punctuation
    citation = ", ".join(parts)

    # Clean up multiple spaces and ensure proper ending
    citation = " ".join(citation.split())
    if citation and not citation.endswith("."):
        citation += "."

    return citation
