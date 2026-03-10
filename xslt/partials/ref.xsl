<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:template name="ref" match="tei:ref">
      <xsl:variable name="id" select="replace($target, '^#', '')"/>
        <a href="{concat($base_url, $id)}"><xsl:apply-templates/></a>
    </xsl:template>
</xsl:stylesheet>
