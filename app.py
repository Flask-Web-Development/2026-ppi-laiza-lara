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

from flask import render_template

@app.route("/home")
def home():
    return render_template("index.html", name="Flask")

from flask import request

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return f"Usuário: {request.form['username']}"
    return "Envie um formulário"

from flask import redirect, abort, url_for

@app.route("/go")
def go():
    return redirect(url_for("hello"))

@app.route("/erro")
def erro():
    abort(404)