from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Rasa server URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Cradle AI chatbot!"})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Payload for Rasa server
    payload = {
        "sender": "user",  # You can customize sender id if needed
        "message": user_message
    }

    # Send POST request to Rasa server
    try:
        response = requests.post(RASA_SERVER_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    # Extract Rasa responses
    rasa_responses = response.json()
    bot_messages = [res['text'] for res in rasa_responses if 'text' in res]

    if not bot_messages:
        return jsonify({"error": "No response from bot"}), 500

    return jsonify({"responses": bot_messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

