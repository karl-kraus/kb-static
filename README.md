# Karl Kraus Bibliographie

* data is fetched from https://github.com/karl-kraus/kb-data
* build with [DSE-Static-Cookiecutter](https://github.com/acdh-oeaw/dse-static-cookiecutter)

## development
* clone the repo
* run `./shellscripts/fetch_data.sh`
* run `./shellscripts/process_data.sh`
* run `ant`

## js-development
* for elaborate JS-development you can start a vite server
```shell
npm install
npm run dev
```
* files you'd like to ingest javascript into need to add `<xsl:param name="production"></xsl:param>` into the matching xslt
* as well as below the closing `<body>` tag add something like (be aware to match the name of the `.ts` file)
```xml
<xsl:choose>
    <xsl:when test="lower-case(normalize-space($production)) = ('1', 'true', 'yes', 'on')">
        <script src="assets/charts.js"/>
    </xsl:when>
    <xsl:otherwise>
        <script type="module" src="http://localhost:5173/@vite/client"></script>
        <script type="module" src="http://localhost:5173/src/charts.ts"></script>
    </xsl:otherwise>
</xsl:choose>
```
* now you should have a hot reload server setup
* don't forget to modify the `build.xml` by adding `<param name="production" expression="${production}"/>`, e.g. 
```xml
<xslt in="${index}" out="${target}/charts.html" style="./xslt/charts.xsl">
    <factory name="net.sf.saxon.TransformerFactoryImpl"/>
    <classpath location="${basedir}/saxon/saxon9he.jar"/>
    <param name="production" expression="${production}"/>
</xslt>
```

### start dev server
* open html folder
```shell
cd html
uv run -m http.server
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in browser.

## Licenses

This project is released under the [MIT License](LICENSE)

### third-party JavaScript libraries
The code for all third-party JavaScript libraries used is included in the `html/vendor` folder, their respective licenses can be found either in a `LICENSE.txt` file or directly in the header of the `.js` file

### SAXON-HE
The projects also includes Saxon-HE, which is licensed separately under the Mozilla Public License, Version 2.0 (MPL 2.0). See the dedicated [LICENSE.txt](saxon/notices/LICENSE.txt)

