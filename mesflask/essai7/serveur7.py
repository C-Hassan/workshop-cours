from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    # Affiche le formulaire contenu dans index.html
    return render_template("index.html")

@app.route('/page2', methods=['POST'])
def page2():
    resultat = request.form
    nom = resultat.get('Nom')
    prenom = resultat.get('Prénom')
    choix = resultat.get('accepte')
    nomComplet = f"{nom} {prenom}" 
    
    return render_template("page2.html", nom_complet=nomComplet, choix=choix)

if __name__ == "__main__":
    app.run(debug=True)