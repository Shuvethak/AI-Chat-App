from flask import Flask, request, jsonify
from llm import get_ai_reply

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

    #  CALL THE AI (this is the FIX)
    ai_reply = get_ai_reply(user_message)

    return jsonify({"reply": ai_reply})


if __name__ == "__main__":
    app.run(debug=True)
