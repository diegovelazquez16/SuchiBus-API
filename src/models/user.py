from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
load_dotenv()

class User(db.Model):
    __tablename__ = 'users'
    schema_name = os.getenv('SCHEMA_NAME')
    __table_args__ = {'schema': schema_name}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tipo_usuario = db.Column(db.String(50))  

    def __init__(self, nombre, email, password, tipo_usuario):
        self.nombre = nombre
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.tipo_usuario = tipo_usuario

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.nombre}>'


class Pasajero(User):
    __tablename__ = 'pasajeros'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    edad = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pasajero',
    }

class Chofer(User):
    __tablename__ = 'choferes'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    licencia = db.Column(db.String(100), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'chofer',
    }

class Administrador(User):
    __tablename__ = 'administradores'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'administrador',
    }
