from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/process_data": {"origins": "http://localhost:3000"}})

# Set your OpenAI API key
openai.api_key = ''

messages = []

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    user_message = data.get('user_message')

    # Check if the user_message is a valid string
    if not isinstance(user_message, str):
        return jsonify({"error": "Invalid user message"})

    # Create a message for the user
    user_input = {"role": "user", "content": user_message}
    messages.append(user_input)

    # Get a response from the GPT-3 model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)

    # Extract the reply from the GPT-3 model's response
    reply = response["choices"][0]["message"]["content"]

    # Add the assistant's reply to the messages
    assistant_reply = {"role": "assistant", "content": reply}
    messages.append(assistant_reply)

    # Return the assistant's reply to the client
    return jsonify({"response": reply})


if __name__ == '__main__':
    app.run(debug=True)
