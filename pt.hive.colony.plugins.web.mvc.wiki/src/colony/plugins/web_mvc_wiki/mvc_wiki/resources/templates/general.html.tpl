${include file="doctype.html.tpl" /}
<head>
    <title>Hive Solutions - The diary</title>
    ${include file="includes.html.tpl" /}
</head>
<body>
    ${include file="header.html.tpl" /}
    <div id="wiki-contents">
        ${out value=page_contents /}
    </div>
    ${include file="footer.html.tpl" /}
</body>
${include file="end_doctype.html.tpl" /}
