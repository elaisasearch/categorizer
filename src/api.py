"""
The Application Programming Interface (API) for the entire Search Engine.
"""

import json
from bottle import Bottle, request, response, run, template
from categorize_en import categorizeText

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
    return template('index')


@app.route('/getlanguagelevel', method=["OPTIONS", "GET"])
def getLanguageLevel() -> dict:
    """
    Takes the user input and returns the found documents as dictionary.
    :text: String
    :return: Dictionary
    """
    text: str = request.params.get('text')

    return {
        "result": categorizeText(text)
    }


app.run(host='0.0.0.0', port=8081, debug=True, reloader=True)