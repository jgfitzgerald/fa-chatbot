from flask import Flask, abort, request, jsonify
from bot import Chatbot
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = {}

# TODO api calls, optimize yaml formatting, store and update user info

@app.route('/app/chat', methods=['POST'])
def chat():
    if request.json['id'] not in db:
         abort(404)
    else:
        user_input = request.json['input']
        response = db.get(request.json['id']).handle_input(user_input)
        return jsonify(response)

@app.route('/app/start', methods=['POST'])
def start():
    convo = {
        'id': "testing",
        'ice': {
            'says': ["Hi", "Would you like banana or ice cream?"],
            'reply': [
                {
                    'question': "Banana",
                    'answer': "NEW BRUNSWICK"
                },
                {
                    'question': "Ice Cream",
                    'answer': "ice-cream"
                }
            ]
        },
        'ice-cream': {
            'says': ["🍦"],
            'reply': [
                {
                    'question': "Start Over",
                    'answer': "ice"
                }
            ]
        }
    }

    return jsonify(convo)

if __name__ == '__main__':
    app.run()


    # Instantiate a new chatbot
    # chatbot = Chatbot()
    # db[str(chatbot.id)] = chatbot
    # bot_response = chatbot.run()
    
    # return jsonify(bot_response)

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run()
