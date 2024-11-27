from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy.dialects.postgresql import JSONB
import json

load_dotenv()

schema_name = os.getenv('SCHEMA_NAME', 'public')  # 'public' como valor por defecto

from .user import db

class Terminal(db.Model):
    __tablename__ = 'terminales'
    __table_args__ = {'schema': schema_name}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(JSONB, nullable=True)
    horarioApertura = db.Column(db.String(100), nullable=False)
    horarioCierre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.BigInteger, nullable=False)
    ruta_id = db.Column(db.String(100), nullable = False)

    def __init__(self, nombre, direccion, horarioApertura, horarioCierre, telefono, ruta_id):
        self.nombre = nombre
        self.horarioApertura = horarioApertura
        self.horarioCierre = horarioCierre
        self.telefono = telefono
        self.ruta_id = ruta_id
        self.direccion = json.dumps(direccion) if direccion else None
    def get_direccion(self):
        return json.loads(self.direccion) if self.direccion else {}