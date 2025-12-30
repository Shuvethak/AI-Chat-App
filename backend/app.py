from flask import Flask, request, jsonify
from llm import get_ai_reply
import os

try:
    from flask_cors import CORS
except ImportError:
    raise RuntimeError(
        "Missing dependency 'flask-cors'. Run:\n"
        "  python -m pip install flask-cors"
    ) from None

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Backend is running!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    # CALL THE AI
    ai_reply = get_ai_reply(user_message)

    return jsonify({"reply": ai_reply})


if __name__ == "__main__":
    # Use Render-assigned PORT and make server externally accessible
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

