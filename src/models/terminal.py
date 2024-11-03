from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

schema_name = os.getenv('SCHEMA_NAME', 'public')  # 'public' como valor por defecto

from .user import db

class Terminal(db.Model):
    __tablename__ = 'terminales'
    __table_args__ = {'schema': schema_name}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    colonia = db.Column(db.String(100), nullable=False)
    calle = db.Column(db.String(100), nullable=False)
    num = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre, ciudad, colonia, calle, num, horario):
        self.nombre = nombre
        self.ciudad = ciudad
        self.colonia = colonia
        self.calle = calle
        self.num = num
        self.horario = horario