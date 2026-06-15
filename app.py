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