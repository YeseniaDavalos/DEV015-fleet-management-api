"""
Este es un ejemplo básico de una aplicación Flask que devuelve 'Hello, World!'.
"""
from flask import Flask, Blueprint, request, jsonify
from app.config import Config
from app.base_de_datos.sql import db
from app.src.models.taxi_model import Taxi
#from app.src.models.routes_trajectories import bp_route_trajectories
from datetime import datetime
from sqlalchemy import func
from app.src.models.trajectory_model import Trajectory

__all__ = ['Taxi', 'Trajectory']

bp_route_home = Blueprint('bp_route_home', __name__)

@bp_route_home.route("/")
def hello():
    return "Hola mundo!!"

bp_route_taxis = Blueprint('bp_route_taxis', __name__)

@bp_route_taxis.route("/taxis", methods=['GET'])
def get_taxis():
    """
    Obtiene una lista de taxis desde la base de datos con opciones de paginación y filtrado.
    """
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    plate = request.args.get('plate', '')

    query = db.session.query(Taxi)
    if plate:
        query = query.filter(Taxi.plate.like(f'%{plate}%'))

    limit = request.args.get('limit', 10)  # Valor predeterminado ajustado
    try:
        limit = int(limit)
        if limit < 1 or limit > 10:
            limit = per_page
    except ValueError:
        limit = per_page

    taxis = query.offset((page - 1) * per_page).limit(limit).all()

    return jsonify([taxi.to_dict() for taxi in taxis])

bp_route_trajectories = Blueprint('bp_route_trajectories', __name__)

@bp_route_trajectories.route("/trajectories", methods=['GET'])
def get_trajectories() :

    """
    Obtiene una lista de trayectorias de un taxi desde la base de datos.

    La ruta responde a una solicitud GET y requiere los parámetros obligatorios 
    `taxiId` y `date` para filtrar las trayectorias del taxi en una fecha específica.

    Query Params:
    taxiId (int, requerido): El ID del taxi para obtener sus trayectorias.
    date (str, requerido): La fecha específica para en formato DD-MM-YYYY.

    Returns:
    Una lista de diccionarios que representan las trayectorias del taxi en la fecha proporcionada.
    Si no encuentra trayectorias o faltan parámetros, devuelve un mensaje de error en formato JSON.
    
    Status Codes:
    400: Faltan parámetros requeridos o el formato de la fecha es incorrecto.
    404: No se encontraron trayectorias para el taxi y la fecha proporcionados.
    """

    taxi_id = request.args.get('taxiId', '')
    if not taxi_id:
        return jsonify({"error": "El ID del taxi es obligatorio"}), 400

    date = request.args.get('date')

    if not date:
        return jsonify({"error": "La fecha es obligatoria"}), 400
    try:
        date = datetime.strptime(date, '%d-%m-%Y')

    except ValueError:
        return jsonify({"error": "Fecha invalida, por favor usa el formato DD-MM-YYYY"}), 400

    query = db.session.query(Trajectory)

    trajectories = query.filter(
    Trajectory.taxi_id == taxi_id,
    func.date(Trajectory.date) == date.date()  # Comparar solo la fecha sin la hora
    ).all()

    if not trajectories:
        return jsonify({"error": "No se encontraron trayectorias"}), 404
    
    return jsonify([trajectory.to_dict() for trajectory in trajectories])

bp_route_latest = Blueprint('bp_route_latest', __name__)

@bp_route_latest.route('/trajectories/latest', methods=['GET'])
def get_latest_trajectories():

    # Subconsulta que obtiene la última trayectoria por taxi_id
    subquery = db.session.query(
        Trajectory.taxi_id,
        #func max (funcion de sql) .label(renombra el resultado de una función)
        func.max(Trajectory.date).label('latest_trajectories') 
        #group_by (agrupa los resultados de cada taxi con su ultima trayectoria)
    ).group_by(Trajectory.taxi_id).subquery()

    last_trajectories = db.session.query(
        Taxi.id,
        Taxi.plate,
        Trajectory.date,
        Trajectory.latitude,
        Trajectory.longitude
    ).join(Trajectory, Taxi.id == Trajectory.taxi_id)\
    .filter(Trajectory.taxi_id == subquery.c.taxi_id)\
    .filter(Trajectory.date == subquery.c.latest_trajectories).distinct()\
    .all()

    if not last_trajectories:
        return jsonify({ "error": "Ultimas rutas no encontradas" }), 404

    dict_latest_trajectories = []
    for trajectory in last_trajectories:
        dict_latest_trajectories.append({
            'id': trajectory.id,  # Aquí añades la propiedad 'id'
            'taxiId': trajectory.id,              # Taxi ID
            'plate': trajectory.plate,            # Placa del taxi
            'date': trajectory.date,         # Fecha de la última trayectoria
            'latitude': trajectory.latitude,      # Latitud
            'longitude': trajectory.longitude     # Longitud
        })

    return jsonify(dict_latest_trajectories), 200

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  
    db.init_app(app)  

    app.register_blueprint(bp_route_home)
    app.register_blueprint(bp_route_taxis)
    app.register_blueprint(bp_route_trajectories)
    app.register_blueprint(bp_route_latest)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app



fleat_app = create_app()

if __name__ == '__main__':
    fleat_app.run(host='0.0.0.0', port=8000)

# Añadir una línea en blanco al final del archivo
