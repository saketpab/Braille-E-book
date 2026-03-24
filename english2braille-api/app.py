from flask import Flask
from flask import request
from updatedBrailleTranslator import arrayWordOrSign as tra2
from updatedBrailleTranslator import getNextWord as gNW
from translate import translate as tra

app = Flask(__name__)


@app.route('/translate', methods=['POST'])
def translate():
    d = request.get_json(force=True)
    return {
        "response": gNW(tra2(d['translate']))
    }


@app.route('/translate1', methods=['POST'])
def translate1():
    d = request.get_json(force=True)
    return {
        "response": tra(d['translate'])
    }


if __name__ == '__main__':
    app.run()
