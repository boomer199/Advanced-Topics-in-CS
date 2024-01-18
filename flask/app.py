from flask import Flask, request, render_template, send_from_directory, send_file

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, I am a machine."

@app.route("/bob/<username>")
def bob(username):
    name =request.args.get("name")
    items = ["banana", "cones", "evritt", "snow"]
    return render_template("hello.html", user = name, items = items)


@app.route("/portfolio")
def portfolio():
    return send_file("./static/index.htm")

@app.errorhandler(404)
def error():
    return


app.run()

