
from flask import Flask, request, jsonify, send_from_directory
from laya import Router

app = Flask(__name__)

# Initialize Laya router
router = Router()

# Define query categories
questions = {
    "intent": {
        "type": "choice",
        "instructions": "Choose the main intent of the user's message.",
        "criteria": {
            "greeting": (
                "The user greets the chatbot, says hello, hi, "
                "good morning, or asks how it is doing."
            ),
            "technical": (
                "The user asks about Python, programming, coding errors, "
                "software, databases, AI, machine learning, or technology."
            ),
            "general": (
                "The user asks a general knowledge question or wants "
                "an explanation of a topic, concept, or definition."
            ),
            "other": (
                "The message does not match any other category."
            ),
        },
    }
}


def create_reply(intent, user_text):
    """Generate a predefined reply based on the detected intent."""

    if intent == "greeting":
        return "Hello! How can I help you today?"

    elif intent == "technical":
        return (
            "That is a technical question. I can help with "
            "programming, AI, machine learning, and software concepts. "
            "What would you like to learn?"
        )

    elif intent == "general":
        return (
            "I can help with general questions. "
            "Please tell me what you want to know."
        )

    else:
        return (
            "I am not sure which category your request belongs to. "
            "Please explain your question in a different way."
        )


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_text = data.get("question", "").strip()

    if not user_text:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        result = router.predict(user_text, questions)
        intent = result["answers"]["intent"]["choice"]

        reply = create_reply(intent, user_text)

        return jsonify({
            "reply": reply,
            "intent": intent
        })

    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({
            "error": "The chatbot could not process your request."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
