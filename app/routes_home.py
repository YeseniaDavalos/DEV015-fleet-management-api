"""
Este módulo define rutas para el home utilizando Flask's Blueprint.
"""

from flask import Blueprint

bp_route_home = Blueprint('bp_route_home', __name__)

@bp_route_home.route("/")
def hello():
    """
    Función que devuelve un mensaje de saludo.
    """
    return "¡Hola mundo!"
