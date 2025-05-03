from flask import Flask, request, render_template
from chatBot import get_bot_reply

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chat():
    user_input = ""
    bot_reply = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_reply = get_bot_reply(user_input)
    return render_template("index.html", user_input=user_input, bot_reply=bot_reply)

if __name__ == "__main__":
    app.run(debug=True)