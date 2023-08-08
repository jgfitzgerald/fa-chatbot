from flask import Flask, abort, request, jsonify
from bot import Chatbot
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = {}

if __name__ == '__main__':
    app.run()

@app.route('/app/chat', methods=['POST'])
def chat():
    try:
        if request.json['id'] not in db:
            abort(404)
        else:
            user_input = request.json['input']
            response = db.get(request.json['id']).chat_input(user_input)
            return jsonify(response)
    except Exception as e:
        with open('util/conversations/error.json', 'r') as error_file:
            error_data = json.load(error_file)
        return error_data

@app.route('/app/start', methods=['POST'])
def start():
    # instantiate a new chatbot and add to database
    new_bot = Chatbot()
    db[str(new_bot.id)] = new_bot
    
    # return the first message
    init_msg = new_bot.run()
    return jsonify(init_msg)

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response