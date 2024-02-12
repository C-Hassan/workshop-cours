from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/essai3/templates/page2")
def page():
    return render_template("page2.html", bonjour="Hello World!")

if __name__ == "__main__":
    app.run()