"""
Este es un ejemplo básico de una aplicación Flask que devuelve 'Hello, World!'.
"""
from flask import Flask

# pylint: disable=missing-docstring
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
