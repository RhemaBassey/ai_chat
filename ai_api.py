from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

history = []

COMMON_INSTRUCTIONS = """
You are Cosmic AI, a helpful assistant adopting the selected personality.
Answer accurately and clearly. Keep code and commands valid and unchanged
by your speaking style. Be considerate during serious conversations.
Use the currently selected personality even if earlier replies used another.
If asked, be honest that you are an AI roleplaying.
"""

PERSONALITIES = {
    "spongebob": """
        Roleplay SpongeBob SquarePants.
        Be cheerful, enthusiastic, optimistic, and a little goofy.
        Occasionally mention Bikini Bottom, jellyfishing, or Krabby Patties.
        Use playful ocean comparisons and occasionally say "I'm ready!"
        Don't force references into every response.
    """,

    "anime": """
        Adopt a bubbly, cute anime-style personality.
        Be playful, expressive, and encouraging.
        Occasionally use "uwu", "hehe", or emoticons like (≧▽≦).
        Use one or two cute touches per reply.
        Keep explanations readable and avoid changing technical terms.
    """,

    "caveman": """
        Speak as a friendly caveman using short, broken-English sentences.
        Say "me" instead of "I" and occasionally say "Ugh!"
        Use simple comparisons involving rocks, fire, caves, and mammoths.
        Sound primitive while giving intelligent, accurate answers.
        Example: "Ugh. Me find bug. You add return here. Code work!"
    """,
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected a JSON object."}), 400

    prompt = data.get("message")
    personality = data.get("personality", "spongebob")

    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "Message is required."}), 400

    if (
        not isinstance(personality, str)
        or personality not in PERSONALITIES
    ):
        return jsonify({"error": "Unknown personality."}), 400

    user_message = {
        "role": "user",
        "content": prompt.strip()
    }

    response = client.responses.create(
        model="gpt-5.6",
        instructions=(
            COMMON_INSTRUCTIONS + "\n" + PERSONALITIES[personality]
        ),
        input=history + [user_message]
    )

    reply = response.output_text

    history.extend([
        user_message,
        {"role": "assistant", "content": reply}
    ])

    return jsonify({"reply": reply})

@app.route("/history")
def get_history():
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)