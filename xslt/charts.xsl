<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="2.0" exclude-result-prefixes="xsl tei xs">
    <xsl:output encoding="UTF-8" media-type="text/html" method="html" version="5.0" indent="yes" omit-xml-declaration="yes"/>
    
    <xsl:import href="./partials/html_navbar.xsl"/>
    <xsl:import href="./partials/html_head.xsl"/>
    <xsl:import href="./partials/html_footer.xsl"/>
    <xsl:import href="./partials/blockquote.xsl"/>
    <xsl:import href="partials/zotero.xsl"/>

    <xsl:template match="/">
        <xsl:variable name="doc_title" select="'Charts'"/>
        
        
        <html class="h-100" lang="{$default_lang}">
            <head>
                <xsl:call-template name="html_head">
                    <xsl:with-param name="html_title" select="$doc_title"></xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="zoterMetaTags">
                    <xsl:with-param name="pageId" select="'charts.html'"></xsl:with-param>
                    <xsl:with-param name="zoteroTitle" select="$doc_title"></xsl:with-param>
                </xsl:call-template>
            </head>
            
            <body class="d-flex flex-column h-100">
            <xsl:call-template name="nav_bar"/>
                <main class="flex-shrink-0 flex-grow-1">
                    <nav style="--bs-breadcrumb-divider: '>';" aria-label="breadcrumb" class="ps-5 p-3">
                        <ol class="breadcrumb">
                            <li class="breadcrumb-item">
                                <a href="index.html">
                                    <xsl:value-of select="$project_short_title"/>
                                </a>
                            </li>
                            <li class="breadcrumb-item active" aria-current="page">
                                <xsl:value-of select="$doc_title"/>
                            </li>
                        </ol>
                    </nav>
                    <div class="container">                        
                        <h1>
                            <xsl:value-of select="$doc_title"/>
                        </h1>
                        <div class="pt-3">
                            <div class="d-flex align-items-center justify-content-between gap-3">
                                <h2 class="mb-0">Texte pro Jahr</h2>
                                <button class="btn btn-outline-secondary btn-sm" type="button" data-chart-reset="bibl-per-year">Reset zoom</button>
                            </div>
                            <canvas class="pt-2" data-chart-type="bar" id="bibl-per-year"></canvas>
                        </div>

                        <div class="pt-3">
                            <div class="d-flex align-items-center justify-content-between gap-3">
                                <h2 class="mb-0">Texte pro Autor*in</h2>
                                <button class="btn btn-outline-secondary btn-sm" type="button" data-chart-reset="bibl-per-author">Reset zoom</button>
                            </div>
                            <canvas class="pt-2" data-chart-type="bar" id="bibl-per-author"></canvas>
                        </div>

                        <div class="pt-3">
                            <div class="d-flex align-items-center justify-content-between gap-3">
                                <h2 class="mb-0">Texte pro Ort</h2>
                                <button class="btn btn-outline-secondary btn-sm" type="button" data-chart-reset="bibl-per-place">Reset zoom</button>
                            </div>
                            <canvas class="pt-2" data-chart-type="bar" id="bibl-per-place"></canvas>
                        </div>


                        <div class="text-center p-4">
                            <xsl:call-template name="blockquote">
                                <xsl:with-param name="pageId" select="'charts.html'"/>
                            </xsl:call-template>
                        </div>
                    </div>
                </main>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/hammerjs@2.0.8"></script>
                <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@2.2.0/dist/chartjs-plugin-zoom.min.js"></script>
                <script src="js/charts/bar-charts.js"/> 
                <xsl:call-template name="html_footer"/>
            </body>
        </html>
    </xsl:template> 
</xsl:stylesheet>
