from flask import jsonify, request, send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from src.controllers.driveController import upload_to_drive, download_from_drive
import tempfile
import os
import re
from io import BytesIO

def crear_usuario(data, file):
    if not file:
        return jsonify({"mensaje": "Se requiere un archivo para la imagen del usuario"}), 400

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    try:
        file_id = upload_to_drive(file_path, file.filename)
        google_drive_url = f"https://drive.google.com/uc?id={file_id}"
    except Exception as e:
        os.remove(file_path)
        return jsonify({"mensaje": f"Error al subir la imagen: {str(e)}"}), 500

    os.remove(file_path)

    nuevo_usuario = User(
        nombre=data.get("nombre"),
        email=data.get("email"),
        password=data.get("password"),  
        tipo_usuario=data.get("tipo_usuario"),
        imagen_url=google_drive_url,
    )
    
    nuevo_usuario.imagen_url = google_drive_url

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "mensaje": "Usuario creado con éxito",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "tipo_usuario": nuevo_usuario.tipo_usuario,
        "imagen_url": nuevo_usuario.imagen_url
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



def obtener_usuario_por_id(user_id):
    """
    Obtener un usuario por su ID.
    """
    try:
        usuario = User.query.get(user_id)

        if not usuario:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        return jsonify({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario
        }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error al obtener el usuario", "error": str(e)}), 500


@jwt_required()
def actualizar_usuario():
    user_id = get_jwt_identity() 
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404  

    data = request.form  
    file = request.files.get('imagen')  

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
        tipos_validos = ["Administrador", "Pasajero", "Chofer"]
        if tipo_usuario not in tipos_validos:
            return jsonify({"mensaje": f"Tipo de usuario inválido. Debe ser uno de: {', '.join(tipos_validos)}"}), 400
        user.tipo_usuario = tipo_usuario

    if file:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path) 

        file_id = upload_to_drive(file_path, file.filename)
        user.imagen_url = f"https://drive.google.com/uc?id={file_id}" 

        os.remove(file_path)  

    db.session.commit()  

    return jsonify({
        "mensaje": "Datos del usuario actualizados",
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "tipo_usuario": user.tipo_usuario,
        "imagen_url": user.imagen_url
    }), 200

@jwt_required()
def eliminar_usuario(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"mensaje": "Usuario eliminado"}), 200
@jwt_required()
def obtener_imagen_usuario(id):
    try:
        usuario = User.query.get(id)
        if usuario is None:
            return jsonify({"error": "Usuario no encontrado"}), 404

        respuesta = {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario,
        }

        if usuario.imagen_url:
            try:
                match = re.search(r'id=([a-zA-Z0-9_-]+)', usuario.imagen_url)
                if match:
                    file_id = match.group(1)
                    file_data = download_from_drive(file_id)
                    return send_file(file_data, mimetype="image/jpeg")

                else:
                    respuesta["imagen_url"] = None
                    respuesta["warning"] = "Formato de imagen_url inválido"
            except Exception as e:
                respuesta["imagen_url"] = None
                respuesta["error"] = f"No se pudo descargar la imagen: {str(e)}"
        else:
            respuesta["imagen_url"] = None  

        return jsonify(respuesta), 200

    except Exception as e:
        return jsonify({"error": "Error procesando la solicitud", "detalle": str(e)}), 500
