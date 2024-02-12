from flask import Flask
app = Flask(__name__)

@app.route('/')
def bonjour():
    return "<p> Hello, hello ! </p>"

if __name__ == '__main__':
    app.run(debug=True)