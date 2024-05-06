from flask import render_template, request, redirect, url_for, jsonify
from app import app
from .utils import generate_description

# Endpoint pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint pour télécharger une image
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Code pour gérer le téléchargement de l'image
        return redirect(url_for("predict"))
    return render_template("upload.html")

# Endpoint pour générer une légende à partir de l'image
@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]

    try:
        description = generate_description(image)
        return jsonify({"description": description}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint pour une route protégée nécessitant une authentification
@app.route("/protected_route", methods=["GET"])
def protected_route():
    token = request.headers.get('Authorization')

    if token != 'your_token':
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"message": "You have access to this route."}), 200
