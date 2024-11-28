from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from sqlalchemy import Enum
import os
import json
from sqlalchemy.dialects.postgresql import JSONB


load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()

schema_name = os.getenv('SCHEMA_NAME', 'public')

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': schema_name}
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    tipo_usuario = db.Column(Enum("Administrador", "Pasajero", "Chofer", name="role_enum"), nullable=False)

    def __init__(self, nombre, email, password, tipo_usuario):
        self.nombre = nombre
        self.email = email
        self.set_password(password)
        self.tipo_usuario = tipo_usuario

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Pasajero(db.Model):
    __tablename__ = 'pasajeros'
    __table_args__ = {'schema': schema_name}
    
    id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.users.id'), primary_key=True)
    edad = db.Column(db.Integer, nullable=True)

    user = db.relationship("User", backref="pasajero", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pasajero',
    }


class Chofer(db.Model):
    __tablename__ = 'choferes'
    __table_args__ = {'schema': schema_name}

    id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.users.id'), primary_key=True)
    username = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    licencia = db.Column(db.String(100))
    imagen_url = db.Column(db.String(400), nullable=True)
    direccion = db.Column(JSONB, nullable=True)
    edad = db.Column(db.Integer)
    experienciaLaboral = db.Column(db.String(50))
    telefono = db.Column(db.String(10))
    status = db.Column(db.String(100))

    user = db.relationship("User", backref="chofer", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'chofer',
    }



class Administrador(db.Model):
    __tablename__ = 'administradores'
    __table_args__ = {'schema': schema_name}
    
    id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.users.id'), primary_key=True)
    username = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    imagen_url = db.Column(db.String(400), nullable=True,)
    direccion = db.Column(JSONB,)
    edad = db.Column(db.Integer)
    telefono= db.Column(db.String(10))
    status= db.Column(db.String(100))
    experienciaLaboral = db.Column(db.String(50))



    user = db.relationship("User", backref="administrador", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'administrador',
    }
