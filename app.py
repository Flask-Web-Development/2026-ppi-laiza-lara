from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, Flask!"

@app.route("/hello")
def hello():
    return "Olá, mundo!"

@app.route("/user/<name>")
def user(name):
    return f"Usuário: {name}"

from markupsafe import escape

@app.route("/escape/<text>")
def escape_text(text):
    return escape(text)