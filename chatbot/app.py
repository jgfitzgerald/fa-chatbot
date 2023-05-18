from flask import Flask, abort, request, jsonify
from bot import Chatbot

app = Flask(__name__)
db = {}

# TODO comments
# TODO api requests and urls

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
    # Instantiate a new chatbot
    chatbot = Chatbot()
    db[str(chatbot.id)] = chatbot
    bot_response = chatbot.run()
    
    return jsonify(bot_response)

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run()
