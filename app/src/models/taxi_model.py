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