<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="2.0" exclude-result-prefixes="xsl tei xs">
    <xsl:output encoding="UTF-8" media-type="text/html" method="html" version="5.0" indent="yes" omit-xml-declaration="yes"/>
    
    <xsl:import href="partials/html_navbar.xsl"/>
    <xsl:import href="partials/html_head.xsl"/>
    <xsl:import href="partials/html_footer.xsl"/>
    <xsl:import href="partials/blockquote.xsl"/>
    <xsl:import href="partials/zotero.xsl"/>

    
    
    <xsl:variable name="teiSource">
        <xsl:value-of select="data(tei:TEI/@xml:id)"/>
    </xsl:variable>
    <xsl:variable name="link">
        <xsl:value-of select="replace($teiSource, '.xml', '.html')"/>
    </xsl:variable>
    <xsl:variable name="doc_title">
        <xsl:value-of select=".//tei:titleStmt/tei:title[2]/text()"/>
    </xsl:variable>


    <xsl:template match="/">
        <html class="h-100" lang="{$default_lang}">
            <head>
                <xsl:call-template name="html_head">
                    <xsl:with-param name="html_title" select="$doc_title"></xsl:with-param>
                </xsl:call-template>
                <xsl:call-template name="zoterMetaTags">
                    <xsl:with-param name="pageId" select="$link"></xsl:with-param>
                    <xsl:with-param name="zoteroTitle" select="$doc_title"></xsl:with-param>
                </xsl:call-template>                
                <meta name="citation_author" content="Scheichl, Sigurd Paul"/> 
                <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js" integrity="sha512-v2CJ7UaYy4JwqLDIrZUI/4hqeoQieOmAZNXBeQyjo21dadnwR+8ZaIJVT8EE2iyI61OV8e6M8PP2/4hpQINQ/g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>

                <link rel="stylesheet" href="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.1/dist/bootstrap-toc.min.css"/>
            </head>
            <body class="d-flex flex-column h-100" data-bs-spy="scroll" data-bs-target="#toc">
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
                        <div class="row">
                            <div class="col-md-2 col-lg-2 col-sm-12 text-start">
                                
                            </div>
                            <div class="col-md-8 col-lg-8 col-sm-12 text-center">
                                <h1>
                                    <xsl:value-of select="$doc_title"/>
                                </h1>
                                <div>
                                    <a href="{$teiSource}">
                                        <i class="bi bi-download fs-2" title="Zum TEI/XML Dokument" visually-hidden="true">
                                            <span class="visually-hidden">Zum TEI/XML Dokument</span>
                                        </i>
                                    </a>
                                </div>
                            </div>
                            <div class="col-md-2 col-lg-2 col-sm-12 text-end">
                                                                
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-3">
                                <details class="d-md-none mb-3 toc-details">
                                    <summary>Table of Contents</summary>
                                    <nav id="toc" data-toggle="toc" class="sticky-top" title="page navigation"></nav>
                                </details>
                                <nav id="toc" data-toggle="toc" class="sticky-top d-none d-md-block" title="page navigation"></nav>
                            </div>
                            <div class="col-md-9">
                            <xsl:for-each-group select=".//tei:body//tei:bibl[./tei:num[@type='category']]" group-by="./tei:num[@type='category']">
                                <h2 class="text-center">
                                    <xsl:value-of select="current-grouping-key()"/> – <xsl:value-of select="current-group()[1]/tei:note[@type='category']"/></h2>
                                <xsl:for-each select="current-group()">
                                    <h3 class="fs-4">
                                        <xsl:value-of select="@n"></xsl:value-of>
                                    </h3>
                                    <dl>
                                        <dt>Kommentar</dt>
                                        <dd><xsl:apply-templates select="./tei:note[@type='comment']"/></dd>
                                    </dl>
                                </xsl:for-each>
                            </xsl:for-each-group>
                        </div>
                        </div>
                        
                        

                        <div class="text-center p-4">
                            <xsl:call-template name="blockquote">
                                <xsl:with-param name="pageId" select="$link"/>
                            </xsl:call-template>
                        </div>

                    </div>
                    
                </main>
                <xsl:call-template name="html_footer"/>
                <script src="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.1/dist/bootstrap-toc.min.js"></script>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
