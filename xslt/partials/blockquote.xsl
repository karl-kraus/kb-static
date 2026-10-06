<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:template name="blockquote">
        <xsl:param name="pageId" select="''"></xsl:param>
        <xsl:param name="customUrl" select="$base_url"></xsl:param>
        <xsl:variable name="fullUrl" select="concat($customUrl, $pageId)"/>
        <div id="how-to-cite">
            <span class="fs-6 fw-bold">How to cite:</span>
            <span class="fs-6">
                Digitale Karl-Kraus-Bibliographie. Digitalisierte Fassung von Sigurd Paul Scheichls
                Kommentierter Auswahlbibliographie zu Karl Kraus. Hrsg. v. Bernhard 
                Oberreither und Peter Andorfer. ACDH. Wien 2025. URL: 
                <a href="{$fullUrl}"><xsl:value-of select="$fullUrl"/></a> (abgerufen am <span id="currentDate"/>).
            </span>
        </div>
        <script>
            document.addEventListener("DOMContentLoaded", function () {
                var el = document.getElementById("currentDate");
                if (!el) return;

                var formatted = new Date().toLocaleDateString("de-DE", {
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                });

                el.textContent = formatted;
            });
        </script>
    </xsl:template>
</xsl:stylesheet>
