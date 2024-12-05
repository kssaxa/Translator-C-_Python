from flask import Flask, request, jsonify,render_template
from flask_cors import CORS

from text_processing.lexer import main

app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    input_text = data.get('text', '')
    tokkens = main(input_text)




    processed_text = tokkens
    return jsonify({'processed_text': processed_text})





if __name__ == '__main__':
    app.run(debug=True)
