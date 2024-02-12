from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def hello():
    return render_template("index.html",
    message_bienvenue = "Bienvenue sur la page d'accueil !")
@app.route("/suivante")
def suite():
    return render_template("page2.html")
app.run()