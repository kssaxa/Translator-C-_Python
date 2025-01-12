from flask import Flask, request, jsonify,render_template
from flask_cors import CORS

from text_processing.lexer import tokenize
from text_processing.semanalizer import Semanalize
from text_processing.sintaxer import Sintaxize

import base64
import json


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])



def process_text():
    data = request.json

    input_text = data.get('text', '')
    tokens = tokenize(input_text)
    tree, str_ast, code = Sintaxize(tokens)
    semantalizer = Semanalize(str_ast)


    # processed_text = tokens
    return jsonify({
        'tokkens':tokens,
        'tree':  tree,
        'semanalize': semantalizer,
        'code': code,
        # 'processed_text': processed_text
    })



@app.route('/getip', methods=['POST', 'GET'])
def getip():
    try:
        with open('ip_address.json', 'r') as file:
            data = json.load(file)
            return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404



# if __name__ == '__main__':
#     app.run(debug=True)
