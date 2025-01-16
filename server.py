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



@app.route('/get_tokkens', methods=['POST'])
def get_tokkens():
    data = request.json
    cpp_code = data.get('code', '')

    try:
        tokens = tokenize(cpp_code)
        tokens_error = False
    except Exception as e:
        tokens = None
        tokens_error = e

    finally:
        return jsonify({
            'tokens': tokens,
            'tokens_error': tokens_error
        })




@app.route('/get_tree', methods=['POST'])
def get_tree():

    data = request.json
    tokens = data.get('tokkens', '')



    try:
        str_tree, ast, code = Sintaxize(tokens)
        tree_error = False
    except Exception as e:
        str_tree, ast, code = None, None, None
        tree_error = e

    return jsonify({
        'tree': str_tree,
        'ast': ast,
        'code': code,
        'tree_error': str(tree_error)
    })









@app.route('/process_text', methods=['POST'])
def process_text():

    cpp_code = None
    cpp_code_read_error = "None"

    tokens = None
    tokens_error = "None"

    str_tree = None
    ast = None
    code = None
    tree_error = "None"
    parser_error = "None"
    ast_error  = "None"
    gener_error = "None"

    semantalizer = None
    semantalizer_error = "None"

    try:
        data = request.json
        cpp_code = data.get('text', '')

        try:
            tokens = tokenize(cpp_code)

            try:
                str_tree, ast, code, parser_error, ast_error, gener_error = Sintaxize(tokens)
                try:
                    semantalizer = Semanalize(ast)
                except Exception as e:
                    semantalizer = None
                    semantalizer_error = str(e)


            except Exception as e:
                tree_error = str(e)


        except Exception as e:
            tokens = None
            tokens_error =  str(e)

    except Exception as e:
        cpp_code_read_error = str(e)



    return jsonify({
        'tokens': tokens,
        'tokens_error': tokens_error,

        'tree': str_tree,
        'tree_error': tree_error,
        'parser_error':parser_error,
        'ast_error':ast_error,
        'gener_error':gener_error,

        'semanalize': semantalizer,
        'semanalizer_error': semantalizer_error,

        'code': code,
        'cpp_code_read_error': cpp_code_read_error,
    })



@app.route('/getip', methods=['POST', 'GET'])
def getip():
    try:
        with open('./ip_address.json', 'r') as file:
            data = json.load(file)
            return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404



# if __name__ == '__main__':
#     app.run(debug=True)
