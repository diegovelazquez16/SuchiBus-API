from flask import Blueprint, request
from src.controllers.userController import actualizar_usuario, crear_usuario, crear_usuario_base, login_usuario, obtener_todos_usuarios, obtener_usuario, eliminar_usuario
from flask_jwt_extended import jwt_required

usuario_blueprint = Blueprint('usuarios', __name__)

@usuario_blueprint.route('/users', methods=['POST'])
def crear_usuario_ruta():
    data = request.get_json()
    return crear_usuario(data)

@usuario_blueprint.route('/users_base', methods=['POST'])
def crear_usuario_base_ruta():
    data = request.get_json()
    return crear_usuario_base(data)

@usuario_blueprint.route('/login', methods=['POST'])
def login_ruta():
    data = request.get_json()
    return login_usuario(data)

@usuario_blueprint.route('/profile', methods=['GET'])
@jwt_required()  
def obtener_usuario_ruta():
    return obtener_usuario()

@usuario_blueprint.route('/users', methods=['GET'])  
def obtener_todos_usuarios_ruta():
    return obtener_todos_usuarios()

@usuario_blueprint.route('/users', methods=['PUT'])  
def actualizar_usuario_ruta():
    return actualizar_usuario()

@usuario_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()  # Requiere autenticación JWT
def eliminar_usuario_ruta(user_id):
    return eliminar_usuario(user_id)
