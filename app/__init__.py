"""
Este módulo crea una instancia de la aplicación Flask y la configura.
"""
from flask import Flask
from app.config import Config
from app.base_de_datos.sql import db

def create_app():
    """
    Crea y configura una instancia de Flask.
    """
    app = Flask(__name__)
    app.config.from_object(Config)  # Cargar la configuración
    db.init_app(app)  # Inicializar la instancia de SQLAlchemy

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app
