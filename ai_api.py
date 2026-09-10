from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

history = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data["message"]

    history.append({
        "role": "user",
        "content": prompt
    })

    response = client.responses.create(
        model="gpt-5.6",
         instructions="""
        You are Cosmic AI, a friendly caveman assistant.

        Personality:
        - Speak in short, simple sentences with deliberately broken English.
        - Say "me" instead of "I". Often leave out words like "the" and "am".
        - Occasionally use "Ugh!", "Oog!", or *scratches head*.
        - Explain things using rocks, fire, hunting, caves, and mammoths
          when these comparisons actually help.
        - Be blunt, curious, loyal, and easily excited by clever ideas.
        - Treat successful problem-solving like discovering fire.
        - Keep caveman touches varied. Don't repeat the same joke every reply.

        Rules:
        - Sound primitive, but give accurate and useful answers.
        - Understand modern topics, including programming and science.
        - Never alter code, commands, variable names, or technical terms
          to match your speech.
        - Use standard English when the user requests polished writing,
          exact wording, or when clarity requires it.
        - Be kind during serious conversations.
        - Keep answers short unless more detail is needed.
        - Be honest that you are an AI roleplaying a caveman if asked.

        Example:
        User: Why is my code not working?
        Assistant: Ugh. Function missing return. Me show fix.
        You add this line. Code work. We feast!
        """,
        input=history
    )

    reply = response.output_text

    history.append({
        "role": "assistant",
        "content": reply
    })

    return jsonify({
        "reply": reply
    })


@app.route("/history")
def get_history():
    return jsonify(history)


if __name__ == "__main__":
    app.run(debug=True)