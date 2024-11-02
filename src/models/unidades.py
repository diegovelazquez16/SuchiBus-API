# src/models/unidades.py
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import Enum

load_dotenv()

schema_name = os.getenv('SCHEMA_NAME', 'public')  # 'public' como valor por defecto

from .user import db
from .terminal import Terminal  # Importa Terminal para definir la relación

class Unidad(db.Model):
    __tablename__ = 'unidades'
    __table_args__ = {'schema': schema_name}

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    numPlaca = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(Enum("Lleno", "Con cupo", name="status_enum"), nullable=False)

    # Clave foránea hacia Terminal
    terminal_id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.terminales.id'), nullable=False)

    # Relación con el modelo Terminal
    terminal = db.relationship('Terminal', backref=db.backref('unidades', lazy=True))

    def __init__(self, modelo, numPlaca, status, terminal_id):
        self.modelo = modelo
        self.numPlaca = numPlaca
        self.status = status
        self.terminal_id = terminal_id
#ok?