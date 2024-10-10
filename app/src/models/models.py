from app import db

class Taxi(db.Model):
    """"
    se crea la tabla taxis
    con la columna id y columna plate
    se convierten en diccionario (JSON)

    """
    __tablename__ = 'taxis'

    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(10))

    def to_dict(self):
        return {
        "id": self.id,
        "plate": self.plate,
        }

class Trajectory(db.Model):

    """"
    se crea la tabla trajectory
    con las columnas id, taxi_id, date, latidude y longitude
    """

    __tablename__ = 'trajectories'

    id = db.Column(db.Integer, primary_key=True)
    taxi_id = db.Column(db.Integer, db.ForeignKey('taxis.id'))
    date = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)