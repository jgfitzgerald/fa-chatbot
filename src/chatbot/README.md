# Chatbot Backend

This file provides an overview of the backend components that handle and return chatbot responses.

## Usage Flow

1. The Flask app (`app.py`) hosts API endpoints to interact with the chatbot.
2. The core chatbot class (`bot.py`) manages conversations, responses, and user inputs.
3. The `response_util.py` file handles dynamic response population based on previous user interactions.
4. The `api_util.py` communicates with an external API to fetch course and location data.

## How to Use

1. Navigate into the `chatbot` directory.
2. Run the Flask app using the command `flask run`.
3. Send POST requests to `/app/start` to initiate a new chatbot session. A response body will include the chatbot response as well as a session UUID.
4. Use the `/app/chat` endpoint to interact with the chatbot. Provide the session UUID and user input in the request payload.

## Customization and Extensibility

- Customize conversation files in the `util/conversations` directory to define different conversation scenarios (see `util/conversations/README.md`).
- Modify the conversation logic in the `bot.py` file to tailor the chatbot's behavior.
- Extend the `Chatbot` class or add new utility functions to integrate additional features such as machine learning or external APIs.

## Examples

- For more examples of conversation structures, refer to the conversation files in the `util/conversations` directory.

---

For more detailed information, refer to the comments in each individual code file. These comments provide a deeper understanding of how each component functions and interacts within the backend.

Feel free to adapt and extend the backend components to create a customized chatbot solution that suits your requirements.