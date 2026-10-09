<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="2.0" exclude-result-prefixes="xsl tei xs">

    <xsl:import href="./partials/html_navbar.xsl"/>
    <xsl:import href="./partials/html_head.xsl"/>
    <xsl:import href="./partials/html_footer.xsl"/>
    <xsl:import href="./partials/blockquote.xsl"/>
    <xsl:import href="./partials/zotero.xsl"/>
    <xsl:import href="./partials/ref.xsl"/>
    <xsl:output encoding="UTF-8" media-type="text/html" method="html" version="5.0" indent="yes"
        omit-xml-declaration="yes"/>

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
                    <xsl:with-param name="html_title" select="$doc_title"/>
                </xsl:call-template>
                <xsl:call-template name="zoterMetaTags">
                    <xsl:with-param name="pageId" select="$link"/>
                    <xsl:with-param name="zoteroTitle" select="$doc_title"/>
                </xsl:call-template>
                <meta name="citation_author" content="Scheichl, Sigurd Paul"/>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js" integrity="sha512-v2CJ7UaYy4JwqLDIrZUI/4hqeoQieOmAZNXBeQyjo21dadnwR+8ZaIJVT8EE2iyI61OV8e6M8PP2/4hpQINQ/g==" crossorigin="anonymous" referrerpolicy="no-referrer"/>

                <link rel="stylesheet"
                    href="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.1/dist/bootstrap-toc.min.css"
                />
                <style>
                    nav.js-toc .nav-link + ul {
                        display: block;
                    }
                </style>
            </head>
            <body class="d-flex flex-column h-100" data-bs-spy="scroll" data-bs-target="#toc">
                <xsl:call-template name="nav_bar"/>
                <main class="flex-shrink-0 flex-grow-1">
                    <nav style="--bs-breadcrumb-divider: '>';" aria-label="breadcrumb"
                        class="ps-5 p-3">
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
                            <div class="col-md-2 col-lg-2 col-sm-12 text-start"> </div>
                            <div class="col-md-8 col-lg-8 col-sm-12 text-center">
                                <h1 data-toc-skip="true">
                                    <xsl:value-of select="$doc_title"/>
                                </h1>
                                <div>
                                    <a href="{$teiSource}">
                                        <i class="bi bi-download fs-2" title="Zum TEI/XML Dokument"
                                            visually-hidden="true">
                                            <span class="visually-hidden">Zum TEI/XML
                                                Dokument</span>
                                        </i>
                                    </a>
                                </div>
                            </div>
                            <div class="col-md-2 col-lg-2 col-sm-12 text-end"> </div>
                        </div>
                        <div class="row">
                            <div class="col-md-3">
                                <details class="d-md-none mb-3 toc-details">
                                    <summary>Table of Contents</summary>
                                    <nav id="toc" class="js-toc sticky-top"
                                        title="page navigation"/>
                                </details>
                                <nav id="toc" class="js-toc sticky-top d-none d-md-block"
                                    style="max-height: calc(100vh - 2rem); overflow-y: auto;"
                                    title="page navigation"/>
                            </div>
                            <div class="col-md-9">
                                <div class="pb-3" id="toc-content">
                                    <xsl:for-each select=".//tei:body/tei:desc">
                                        <xsl:variable name="category">
                                            <xsl:value-of select="tokenize(@corresp)[1]"/>
                                        </xsl:variable>
                                        <xsl:choose>
                                            <xsl:when test="@type='chapter'">
                                                <h2 id="{$category}"><xsl:value-of select="$category"/> – <xsl:value-of select="./text()"/></h2>
                                            </xsl:when>
                                            <xsl:when test="@type='subchapter'">
                                                <h3 id="{$category}"><xsl:value-of select="$category"/> – <xsl:value-of select="./text()"/></h3>
                                            </xsl:when>
                                        </xsl:choose>
                                        <xsl:for-each select="//tei:body//tei:bibl[./tei:num[@type='category']/text() eq $category]">
                                            <h4 class="fs-4" id="{@xml:id}">
                                                <xsl:value-of select="@n"/>
                                            </h4>
                                            <dl>
                                                <dt>Kommentar</dt>
                                                <dd>
                                                    <xsl:apply-templates
                                                        select="./tei:note[@type = 'comment']"/>
                                                </dd>
                                                <dt>KAB-Nummer</dt>
                                                <dd><a href="{@xml:id||'.html'}"><xsl:value-of select="@xml:id"/></a></dd>
                                            </dl>
                                        </xsl:for-each>
                                        <xsl:if test="//tei:body/tei:note[@corresp = $category]">
                                            <h4 class="text-center pt-3">Außerdem</h4>
                                            <xsl:for-each
                                                select="//tei:body/tei:note[@corresp = $category]">
                                                <p>
                                                    <xsl:apply-templates/>
                                                </p>
                                            </xsl:for-each>
                                        </xsl:if>
                                    </xsl:for-each>
                                </div>
                                
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
                <script src="https://cdn.rawgit.com/afeld/bootstrap-toc/v1.0.1/dist/bootstrap-toc.min.js"/>
                <script>
                    $(function () {
    $("nav[id='toc']").each(function () {
    Toc.init({
      $nav: $(this),
      $scope: $("#toc-content")
    });
  });
});
                </script>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
