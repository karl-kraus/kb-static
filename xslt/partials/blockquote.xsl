<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:template name="blockquote">
        <xsl:param name="pageId" select="''"></xsl:param>
        <xsl:param name="customUrl" select="$base_url"></xsl:param>
        <xsl:variable name="fullUrl" select="concat($customUrl, $pageId)"/>
        <div class="mt-5">
                  <span class="fs-5 fw-bold">How to cite:</span>
                  <span class="fs-5">
                     Digitale Karl-Kraus-Bibliographie. Basierend auf Sigurd Paul Scheichls
                      Kommentierter Auswahlbibliographie zu Karl Kraus. Hrsg. v. Bernhard 
                      Oberreither und Peter Andorfer. ACDH. Wien 2025. URL: 
                      <a href="{$fullUrl}"><xsl:value-of select="$fullUrl"/></a>
                  </span>
               </div>
    </xsl:template>
</xsl:stylesheet>
