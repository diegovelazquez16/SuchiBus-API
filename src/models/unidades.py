from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import Enum, Date

load_dotenv()

schema_name = os.getenv('SCHEMA_NAME', 'public')  

from .user import db
from .terminal import Terminal 

class Unidad(db.Model):
    __tablename__ = 'unidades'
    __table_args__ = {'schema': schema_name}

    id = db.Column(db.Integer, primary_key=True)
    numPlaca = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(Enum("Lleno", "Con cupo", name="status_enum"), nullable=False) # mantener
    modelo = db.Column(db.String(20), nullable = False)
    marca = db.Column(db.String(20), nullable = False)
    fecha_compra = db.Column(db.String(20), nullable = False)
    imagen_url = db.Column(db.String(400), nullable = False)
    terminal_id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.terminales.id'), nullable=False)

    terminal = db.relationship('Terminal', backref=db.backref('unidades', lazy=True))

    def __init__(self, numPlaca, status, modelo, marca, fecha_compra, imagen_url, terminal_id):
        self.numPlaca = numPlaca
        self.status = status
        self.modelo = modelo
        self.marca = marca
        self.fecha_compra =  fecha_compra
        self.imagen_url = imagen_url  # me faltaba esto xd
        self.terminal_id = terminal_id
