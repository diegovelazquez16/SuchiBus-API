from flask import Blueprint, request
from src.controllers.userController import (
    actualizar_usuario,
    crear_usuario_base,
    login_usuario,
    obtener_todos_usuarios,
    obtener_usuario,
    obtener_usuario_por_id,
    eliminar_usuario, 
    obtener_imagen_usuario,
    actualizar_usuario_base,
    obtener_usuario_actual,
)
from flask_jwt_extended import jwt_required

usuario_blueprint = Blueprint('usuarios', __name__)

# Crear un usuario con bcrypt
#@usuario_blueprint.route('/users', methods=['POST'])
#def crear_usuario_ruta():
 #   data = request.form.to_dict()  
  #  file = request.files.get('file')  

   # return crear_usuario(data, file)

# Crear usuario sin bcrypt
@usuario_blueprint.route('/users_base', methods=['POST'])
def crear_usuario_base_ruta():
    data = request.get_json()
    return crear_usuario_base(data)

@usuario_blueprint.route('/users_base/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario_base_ruta(id_usuario):
    data = request.get_json()
    return actualizar_usuario_base(id_usuario, data)

# Iniciar sesión
@usuario_blueprint.route('/login', methods=['POST'])
def login_ruta():
    data = request.get_json()
    return login_usuario(data)

# Obtener perfil del usuario autenticado
@usuario_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def obtener_usuario_ruta():
    return obtener_usuario()

@usuario_blueprint.route('/usuarios/me', methods=['GET'])
@jwt_required()
def obtener_usuario_actual_ruta():
    return obtener_usuario_actual()


# Obtener todos los usuarios (requiere autenticación)
@usuario_blueprint.route('/users', methods=['GET'])
@jwt_required()
def obtener_todos_usuarios_ruta():
    return obtener_todos_usuarios()

@usuario_blueprint.route('/users/<int:user_id>', methods=['GET'])
def obtener_usuario_por_id_ruta(user_id):
    return obtener_usuario_por_id(user_id)

@usuario_blueprint.route('/users/profile', methods=['PUT'])
@jwt_required()
def actualizar_usuario_ruta():
    return actualizar_usuario()

@usuario_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario_ruta(user_id):
    return eliminar_usuario(user_id)

@usuario_blueprint.route('/users/<int:id>/image', methods=['GET'])
@jwt_required()
def obtener_imagen_usuario_ruta(id):
    return obtener_imagen_usuario(id)

