from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from sqlalchemy import Enum
import os

# Cargar las variables de entorno
load_dotenv()

# Inicializar SQLAlchemy y Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

# Obtener el nombre del esquema desde las variables de entorno
schema_name = os.getenv('SCHEMA_NAME', 'public')  # 'public' como valor por defecto

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': schema_name}
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    tipo_usuario = db.Column(Enum("Administrador", "Pasajero", "Chofer", name="role_enum"), nullable=False) # mantener
    imagen_url = db.Column(db.String(400), nullable=True)  # Nueva columna para la imagen del usuario

    
    def __init__(self, nombre, email, password, tipo_usuario, imagen_url):
        self.nombre = nombre
        self.email = email
        self.set_password(password)  
        self.tipo_usuario = tipo_usuario
        self.imagen_url = imagen_url  # Asignar la URL de la imagen (si existe)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Pasajero(User):
    __tablename__ = 'pasajeros'
    __table_args__ = {'schema': schema_name}
    
    id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.users.id'), primary_key=True)
    edad = db.Column(db.Integer, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pasajero',
    }

class Chofer(User):
    __tablename__ = 'choferes'
    __table_args__ = {'schema': schema_name}
    
    id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.users.id'), primary_key=True)
    licencia = db.Column(db.String(100), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'chofer',
    }

class Administrador(User):
    __tablename__ = 'administradores'
    __table_args__ = {'schema': schema_name}
    
    id = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'administrador',
    }