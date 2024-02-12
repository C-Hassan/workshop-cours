from datetime import date
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

moment = date.today().strftime("%d /%m/%Y")
H = datetime.now().strftime("%H:%M:%S")
bonjour = "Hello World!"

@app.route("/")
def hello():
    return render_template("index.html", bonjour = "Hello World!",
    moment = moment, heure = H)
app.run()
