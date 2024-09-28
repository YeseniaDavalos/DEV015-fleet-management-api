"""
Este módulo inicializa una instancia de SQLAlchemy para manejar  Flask.
"""

from flask_sqlalchemy import SQLAlchemy

# Crear una instancia de SQLAlchemy para interactuar con la base de datos
db = SQLAlchemy()

# Añadir una línea en blanco al final del archivo
