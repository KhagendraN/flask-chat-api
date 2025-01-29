from flask import Flask, request, jsonify, render_template
import os
from mistralai import Mistral

app = Flask(__name__)

# Predefined questions and answers
predefined_answers = {
    "What is your name?": "I am your AI assistant!",
    "How are you?": "I'm just a bot, but I'm here to help!",
    "What can you do?": "I can answer your questions. Try asking me something!"
}

# Mistral AI API Key (Set this as an environment variable for security)
api_key = os.getenv("MISTRAL_API_KEY")  # Load from environment
if not api_key:
    raise ValueError("API key not found! Set MISTRAL_API_KEY in Render.")

api_key = os.getenv("MISTRAL_API_KEY")
if api_key is None:
    raise ValueError("API key not set in environment variables")

model = "mistral-large-latest"
client = Mistral(api_key=api_key)

def ask_mistral(question):
    """Call Mistral AI API if question is not predefined."""
    chat_response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": question}]
    )
    return chat_response.choices[0].message.content.strip()

@app.route("/")
def index():
    return render_template("chat.html")  # This will serve your frontend

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    
    if question in predefined_answers:
        answer = predefined_answers[question]
    else:
        answer = ask_mistral(question)
    
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Port 10000 (Render default)

