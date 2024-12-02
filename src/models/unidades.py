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
    status = db.Column(db.String(50), nullable = False)
    modelo = db.Column(db.String(20), nullable = False)
    marca = db.Column(db.String(20), nullable = False)
    fecha_compra = db.Column(db.String(20), nullable = False)
    num_asientos = db.Column(db.Integer, nullable = False)
    actual_cupo = db.Column(db.Integer, nullable = True)
    hora_salida = db.Column(db.String, nullable = True)
    hora_llegada = db.Column (db.String, nullable = True)
    imagen_url = db.Column(db.String(400), nullable = False)
    terminal_id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.terminales.id'), nullable=False)
    imagen_archivo = db.Column(db.String, nullable = True)

    terminal = db.relationship('Terminal', backref=db.backref('unidades', lazy=True))

    def __init__(self, numPlaca, status, modelo, marca, fecha_compra, num_asientos, actual_cupo, imagen_url, terminal_id, imagen_archivo):
        self.numPlaca = numPlaca
        self.status = status
        self.modelo = modelo
        self.marca = marca
        self.fecha_compra =  fecha_compra
        self.num_asientos = num_asientos
        self.actual_cupo = actual_cupo
        self.imagen_url = imagen_url  # me faltaba esto xd
        self.terminal_id = terminal_id
        self.imagen_archivo = imagen_archivo

