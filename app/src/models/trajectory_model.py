from app.base_de_datos.sql import db



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

    def to_dict(self):
        return {
        "id": self.id,
        "taxiId": self.taxi_id,
        "date": self.date,
        "latitude": self.latitude,
        "longitude": self.longitude
        }