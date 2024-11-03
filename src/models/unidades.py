from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy import Enum

load_dotenv()

schema_name = os.getenv('SCHEMA_NAME', 'public')  

from .user import db
from .terminal import Terminal 

class Unidad(db.Model):
    __tablename__ = 'unidades'
    __table_args__ = {'schema': schema_name}

    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), nullable=False)
    numPlaca = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(Enum("Lleno", "Con cupo", name="status_enum"), nullable=False)

    terminal_id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.terminales.id'), nullable=False)

    terminal = db.relationship('Terminal', backref=db.backref('unidades', lazy=True))

    def __init__(self, modelo, numPlaca, status, terminal_id):
        self.modelo = modelo
        self.numPlaca = numPlaca
        self.status = status
        self.terminal_id = terminal_id
