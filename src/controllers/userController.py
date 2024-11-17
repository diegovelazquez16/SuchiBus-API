from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash


def crear_usuario(data):
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    tipo_usuario = data.get('tipo_usuario')

    # Validar campos obligatorios
    if not nombre or not email or not password or not tipo_usuario:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    # Validar que el tipo de usuario sea uno de los valores permitidos
    tipos_validos = ["Administrador", "Pasajero", "Chofer"]
    if tipo_usuario not in tipos_validos:
        return jsonify({"mensaje": f"Tipo de usuario inválido. Debe ser uno de: {', '.join(tipos_validos)}"}), 400

    # Verificar si el email ya está registrado
    if User.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El email ya está registrado"}), 400

    # Crear el usuario
    nuevo_usuario = User(
        nombre=nombre,
        email=email,
        password=password,
        tipo_usuario=tipo_usuario
    )
    nuevo_usuario.set_password(password)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "mensaje": "Usuario creado con éxito",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "tipo_usuario": nuevo_usuario.tipo_usuario
    }), 201



def crear_usuario_base(data):
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not nombre or not email or not password:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El email ya está registrado"}), 400

    nuevo_usuario = User(nombre=nombre, email=email, password=password, encrypt_password=False)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "mensaje": "Usuario creado sin bcrypt",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email
    }), 201

def login_usuario(data):
    email = data.get('email')
    password = data.get('password')

    print(f"Email ingresado: {email}")  
    print(f"Contraseña ingresada: {password}") 

    user = User.query.filter_by(email=email).first()

    if not user:
        print("No se encontró el usuario.") 
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    if not user.check_password(password):
        print("Contraseña incorrecta.") 
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "token": access_token
    }), 200


@jwt_required()
def obtener_usuario():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email
    }), 200

@jwt_required()
def obtener_todos_usuarios():
    usuarios = User.query.all()

    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario
        })

    return jsonify(usuarios_list), 200

from flask import jsonify
from src.models.user import User, db

def obtener_usuario_por_id(user_id):
    """
    Obtener un usuario por su ID.
    """
    try:
        # Buscar usuario en la base de datos
        usuario = User.query.get(user_id)

        # Si el usuario no existe, devolver un mensaje de error
        if not usuario:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        # Devolver los datos del usuario
        return jsonify({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario
        }), 200

    except Exception as e:
        # Manejar errores inesperados
        return jsonify({"mensaje": "Error al obtener el usuario", "error": str(e)}), 500


@jwt_required()
def actualizar_usuario():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    tipo_usuario = data.get('tipo_usuario')

    if nombre:
        user.nombre = nombre
    if email:
        # Verificar que el email no esté en uso por otro usuario
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({"mensaje": "El email ya está registrado"}), 400
        user.email = email
    if tipo_usuario:
        # Validar que el nuevo tipo de usuario sea permitido
        tipos_validos = ["Administrador", "Pasajero", "Chofer"]
        if tipo_usuario not in tipos_validos:
            return jsonify({"mensaje": f"Tipo de usuario inválido. Debe ser uno de: {', '.join(tipos_validos)}"}), 400
        user.tipo_usuario = tipo_usuario

    db.session.commit()

    return jsonify({
        "mensaje": "Datos del usuario actualizados",
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "tipo_usuario": user.tipo_usuario
    }), 200
@jwt_required()
def eliminar_usuario(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"mensaje": "Usuario eliminado"}), 200

# Inicio de sesión
def login_usuario(data):
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "token": access_token
    }), 200

@jwt_required()
def obtener_usuario():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "tipo_usuario": user.tipo_usuario
    }), 200

# Obtener todos los usuarios
@jwt_required()
def obtener_todos_usuarios():
    usuarios = User.query.all()
    usuarios_list = [{
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "tipo_usuario": usuario.tipo_usuario
    } for usuario in usuarios]

    return jsonify(usuarios_list), 200

# Actualizar datos del usuario
@jwt_required()
def actualizar_usuario():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    tipo_usuario = data.get('tipo_usuario')

    if nombre:
        user.nombre = nombre
    if email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({"mensaje": "El email ya está registrado"}), 400
        user.email = email
    if tipo_usuario:
        user.tipo_usuario = tipo_usuario

    db.session.commit()

    return jsonify({
        "mensaje": "Datos del usuario actualizados",
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "tipo_usuario": user.tipo_usuario
    }), 200

@jwt_required()
def eliminar_usuario(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"mensaje": "Usuario eliminado"}), 200
