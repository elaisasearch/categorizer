"""
The Application Programming Interface (API) for the Elaisa Categorizer.
"""

import json
from bottle import Bottle, request, response, run, template
from categorize_en import categorizeText
from lib.globals import API_KEY

app = Bottle()


@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route('/')
def index() -> str:
    """
    Root api requst url.
    :return: Template
    """
    return template("""
    <html>
        <body>
            <h2>Categorizer API</h2>
            <b>Method:</b> GET <br />
            <b>URL:</b> https://categorizer.api.elaisa.org/getlanguagelevel?text=your-text <br />
            <b>RESPONSE:</b> { "result": { "level": "A1","difficulty": "hard", "level_meta": { "unknown": 0, "A1": 64, "A2": 0, "B1": 9, "B2": 0, "C1": 0, "C2": 0 } } }
        </body>
    </html>
    """)

@app.route('/getlanguagelevel', method=["OPTIONS", "GET"])
def getLanguageLevel() -> dict:
    """
    Takes the user input and returns the found documents as dictionary.
    :text: String
    :language: String
    :return: Dictionary
    """
    text: str = request.params.get('text')
    language: str = request.params.get('language')

    # check API Key
    if str(request.params.get('key')) != API_KEY:
        response.status = 401
        return {
            "error": "API-KEY is wrong or missing. See https://github.com/elaisasearch/categorizer/blob/master/README.md for more information."
        }

    if language == "en":
        return {
            "result": categorizeText(text)
        }
    # other languages will follow in the future
    else:
        return {
            "error": "'{}' currently isn't supported. Please use 'en' for English as language. Thank you.".format(language) 
        }


app.run(host='0.0.0.0', port=8081, debug=True, reloader=True)