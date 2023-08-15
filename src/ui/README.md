# Chatbot Frontend

This file provides an overview of how to run the frontend of the chatbot, which handles communication with the backend and renders chatbot and user messages.

## Usage Flow

The frontend of the chatbot application consists of three main components that work together to provide an interactive chat experience:

1. **`index.html`**
   The `index.html` file serves as the main webpage containing the chatbot toggle button and the chat window. It provides the user interface elements necessary to interact with the chatbot.

2. **`script.js`**
   The `script.js` file is responsible for handling various event listeners and functions related to the chatbot's behavior. It plays a crucial role in the initialization of the chatbot, opening the chat window, and managing user interactions.

   Key Responsibilities:
   - Initialize the chat window by constructing a `Bubbles` instance.
   - Handle the event when the chatbot toggle button is clicked.
   - Fetch the conversation flow from the backend API to start the chat.
   - Enable the resizing and reloading functionality of the chat window.

3. **`component/Bubbles.js`**
   The `Bubbles.js` file contains the core logic for rendering chat bubbles, handling user input, and managing the conversation flow. It plays a vital role in creating an interactive conversation experience with the chatbot.

   Key Responsibilities:
   - Construct and initialize the `Bubbles` function with configurable options.
   - Manage the display and behavior of user input text field.
   - Handle the conversation flow by displaying chat bubbles for bot messages.
   - Provide options for users to select from predefined buttons.
   - Manage the "typing" indicator during chatbot processing.
   - Handle user input, including clicking on buttons and submitting text input.

By combining these components, the chatbot frontend creates an engaging and dynamic conversation interface that allows users to interact with the chatbot, receive responses, and select options presented in the chat bubbles.

## How to Use

1. Navigate to the `ui` directory.
2. Run the frontend using the command `serve` or `yarn start`
3. Your chatbot webpage will be hosted on `localhost:3000`

---

## Acknowledgements

The frontend for this project is built upon the foundation of the [`chat-bubble`](https://github.com/dmitrizzle/chat-bubble) framework, which provides a simple and lightweight solution for creating chat interfaces, and is liscensed under the MIT liscense. The framework was developed by [dmitrizzle](https://github.com/dmitrizzle). 

For more information about the `chat-bubble` framework, please visit the [GitHub repository](https://github.com/dmitrizzle/chat-bubble).
