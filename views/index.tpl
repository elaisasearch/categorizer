<html>
    <head>
        <title>Elaisa Search Engine - API</title>
        <meta name=”description” content="Elaisa API for accessing language level search engine data. Contact info@elaisa.org for more information.">
    </head>
    <body style="text-align: center;
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        font-size: 17px;
        font-family: Helvetica;"
    >     
        <div style="flex: 1; margin-top: 5%;">
            <a href="https://elaisa.org"><img src="https://raw.githubusercontent.com/dasmemeteam/language-level-search-engine/master/services/service-ui/src/assets/img/logo.png" alt="elaisa api image" width="300"/></a>
            <h1>Elaisa API</h1>
            <h3>Welcome to the Elaisa Categorizer API</h3>
        </div>  
        <div style="flex: 1;">
            Use the /getlanguagelevel GET endpoint to get the language level meta data for your text.

            GET
            https://categorizer.api.elaisa.org/getlanguagelevel?text=your text ...
        </div>
        <div style="
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            border-top: 1px solid rgba(0, 0, 0, 0.2);
            width: 100%;
            margin: 0 auto;
            background: rgb(239,239,239);"
        >
            <p>If you need an API key, please contact <a href="mailto:info@elaisa.org">info@elaisa.org</a>.</p>
        </div>
    </body>
</html>