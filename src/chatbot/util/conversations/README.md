# Chatbot JSON Conversation Scripting

This file provides an overview of the conversation structure used in the chatbot JSON conversation files.

## Conversation Structure

The chatbot conversations are organized in a structured format, allowing the chatbot to respond to user inputs and questions using a text-matching system. Each conversation follows a similar structure to gather and respond to user input:

```json
{
    "get_format": {
        "says": ["Were you looking to take an online, hybrid, or in-person course?"],
        "response_key": "format",
        "reply": [
            {
                "question": "Online",
                "answer": "find-course-dates/get_course_name.json"
            },
            {
                "question": "In-Person",
                "answer": "find-course-dates/get_course_name.json"
            },
            {
                "question": "Hybrid",
                "answer": "find-course-dates/get_course_name.json"
            },
            {
                "question": "What's the difference?",
                "answer": "hybrid_online_explanation"
            }
        ]
    },
    // ... (other conversations in the JSON file)
}
```

### Explanation of Conversation Fields

- `"get_format"`: The identifier for the conversation step.
- `"says"`: An array of messages the chatbot will say to the user at this step.
- `"response_key"`: The key used to identify the user's response to this conversation step, can be omitted if user's response does not need to be stored.
- `"reply"`: An array of potential user replies that the chatbot can handle.

## How to Use Conversations

1. The chatbot responds with the messages in the `"says"` array.
2. The user's response is identified using the `"response_key"` and is stored on the backend.
3. The chatbot then matches the user's response with the corresponding entry in the `"reply"` array.
4. If a match is found, the chatbot uses the associated `"answer"` JSON file or chat conversation identifier to return a response. 

The `"answer"` field can be the path name of a JSON file relative to the `src/chatbot/util/conversations` directory (ex: `"find-course-dates/get_course_name.json"`), or the identifer of a conversation located within the current JSON file, no path name required (ex: `hybrid_online_explanation`).

## Dynamic Response Filling

Refer to src/chatbot/README.md on how to fill responses dynamically based on previously submitted user input.

## Customize and Extend

Feel free to customize and extend the conversations to suit your specific use case. You can add more conversation entries, adjust messages, and create new response files as needed.

## Examples

For more examples and variations of conversation structures, refer to the included JSON data.

---