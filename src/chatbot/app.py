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

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if request.json['id'] not in db:
            abort(404)
        else:
            user_input = request.json['input']
            response = db.get(request.json['id']).chat_input(user_input)
            return jsonify(response)
    except Exception as e:
        print("Exception:", str(e))  # Print the exception
        with open('util/conversations/error.json', 'r') as error_file:
            error_data = json.load(error_file)
        # return an error message to user
        return error_data

@app.route('/api/start', methods=['POST'])
def start():
    # instantiate a new chatbot and add to database
    new_bot = Chatbot()
    db[str(new_bot.id)] = new_bot
    
    # return the first message
    init_msg = new_bot.run()
    return jsonify(init_msg)

@app.route('/api/end', methods=['DELETE'])
def end():
    try:
        chat_id = request.args.get('id')
        
        if chat_id not in db:
            return {"error": f"Chat with ID {chat_id} not found"}, 404
        else:
            # Delete the chat
            del db[chat_id]
            return {"message": f"Chat with ID {chat_id} deleted successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response