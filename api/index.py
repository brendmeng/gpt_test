from flask import Flask, request, jsonify
from flask_cors import CORS
from api.util.engine import ask_and_reply

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return "Hello World"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data['prompt']
    response = ask_and_reply(prompt)
    return jsonify({"response": response})