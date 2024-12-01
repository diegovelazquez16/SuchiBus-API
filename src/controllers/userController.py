from flask import jsonify, request, send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from src.controllers.driveController import upload_to_drive, download_from_drive
import tempfile
import os
import re
from io import BytesIO
from src.models.user import Chofer, Administrador, User
import json
from src.models.terminal import  Terminal, db


def crear_usuario(data, file=None):
    google_drive_url = None  # Por defecto, la imagen no estará presente.

    if file:
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

    tipo_usuario = data.get("tipo_usuario")
    if tipo_usuario not in ["Administrador", "Chofer"]:
        return jsonify({"mensaje": "Tipo de usuario inválido"}), 400
    # Crear el usuario base
    nuevo_usuario = User(
        nombre=data.get("nombre"),
        email=data.get("email"),
        password=data.get("password"),
        tipo_usuario=tipo_usuario,
    )
    db.session.add(nuevo_usuario)
    db.session.flush()

    if tipo_usuario == "Chofer":
        nuevo_chofer = Chofer(
            id=nuevo_usuario.id,
            username=data.get("username"),
            lastname=data.get("lastname"),
            licencia=data.get("licencia"),
            imagen_url=google_drive_url,
            direccion=data.get("direccion"),
            edad=data.get("edad"),
            experienciaLaboral=data.get("experienciaLaboral"),
            telefono=data.get("telefono"),
            status=data.get("status"),
            terminal_id= data.get("terminal_id")
        )
        
        db.session.add(nuevo_chofer)
    elif tipo_usuario == "Administrador":
        nuevo_administrador = Administrador(
            id=nuevo_usuario.id,
            username=data.get("username"),
            lastname=data.get("lastname"),
            imagen_url=google_drive_url,
            direccion=data.get("direccion"),
            edad=data.get("edad"),
            experienciaLaboral=data.get("experienciaLaboral"),
            telefono=data.get("telefono"),
            status=data.get("status"),
        )
        db.session.add(nuevo_administrador)

    db.session.commit()

    response = {
        "mensaje": "Usuario creado con éxito",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "tipo_usuario": nuevo_usuario.tipo_usuario,
    }
    if google_drive_url:
        response["imagen_url"] = google_drive_url

    return jsonify(response), 201





""" def crear_usuario(data, file=None):  # file es ahora opcional

    google_drive_url = None  # Valor predeterminado para la imagen

    if file:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        try:
            # Subir la imagen a Google Drive
            file_id = upload_to_drive(file_path, file.filename)
            google_drive_url = f"https://drive.google.com/uc?id={file_id}"
        except Exception as e:
            os.remove(file_path)
            return jsonify({"mensaje": f"Error al subir la imagen: {str(e)}"}), 500

        # Eliminar archivo temporal
        os.remove(file_path)

    # Validar tipo de usuario
    tipo_usuario = data.get("tipo_usuario")
    if tipo_usuario not in ["Administrador", "Chofer"]:
        return jsonify({"mensaje": "Tipo de usuario inválido"}), 400

    # Crear el usuario base
    nuevo_usuario = User(
        nombre=data.get("nombre"),
        email=data.get("email"),
        password=data.get("password"),
        tipo_usuario=tipo_usuario,
    )
    db.session.add(nuevo_usuario)
    db.session.flush()  # Necesario para obtener el ID del usuario recién creado

    if tipo_usuario == "Chofer":
        nuevo_chofer = Chofer(
            id=nuevo_usuario.id,
            username=data.get("username"),
            lastname=data.get("lastname"),
            licencia=data.get("licencia"),
            imagen_url=google_drive_url,
            direccion=data.get("direccion"),
            edad=data.get("edad"),
            experienciaLaboral= data.get("experienciaLaboral"),
            telefono= data.get("telefono"),
            status = data.get("status")
        )
        db.session.add(nuevo_chofer)
    elif tipo_usuario == "Administrador":
        nuevo_administrador = Administrador(
            id=nuevo_usuario.id,
            username=data.get("username"),
            lastname=data.get("lastname"),
            imagen_url=google_drive_url,
            direccion=data.get("direccion"),
            edad=data.get("edad"),
            experienciaLaboral= data.get("experienciaLaboral"),
            telefono= data.get("telefono"),
            status = data.get("status")
        )
        db.session.add(nuevo_administrador)

    # Confirmar transacción
    db.session.commit()

    # Construir respuesta
    response = {
        "mensaje": "Usuario creado con éxito",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "tipo_usuario": nuevo_usuario.tipo_usuario,
    }
    if google_drive_url:
        response["imagen_url"] = google_drive_url

    return jsonify(response), 201 """


def crear_usuario_base(data):
    
    from src.models.user import Pasajero
    
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not nombre or not email or not password:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El email ya está registrado"}), 400

    nuevo_usuario = User(
        nombre=nombre, 
        email=email, 
        password=password, 
        tipo_usuario="Pasajero"
    )
    
    db.session.add(nuevo_usuario)
    db.session.commit()

    pasajero = Pasajero(id=nuevo_usuario.id)
    db.session.add(pasajero)
    db.session.commit()

    return jsonify({
        "mensaje": "Usuario creado correctamente",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "tipo_usuario": nuevo_usuario.tipo_usuario
    }), 201


    
#@jwt_required()
def actualizar_usuario_base(id_usuario, data):
    usuario = User.query.get(id_usuario)

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')

    if not any([nombre, email, password]):
        return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400

    if nombre:
        usuario.nombre = nombre
    if email:
        if User.query.filter_by(email=email).first() and email != usuario.email:
            return jsonify({"mensaje": "El email ya está registrado"}), 400
        usuario.email = email
    if password:
        usuario.password = password

    db.session.commit()

    return jsonify({
        "mensaje": "Usuario actualizado correctamente",
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email
    }), 200


def login_usuario(data):
    #nombre = data.get('name')
    email = data.get('email')
    password = data.get('password')

    print(f"Email ingresado: {email}")  
    print(f"Contraseña ingresada: {password}") 
    #print(f"nombre ingresado {nombre}")

    user = User.query.filter_by(email=email).first()

    if not user:
        print("No se encontró el usuario.") 
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    if not user.check_password(password):
        print("Contraseña incorrecta.") 
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    #if not nombre:
       # print("usuario incorrecto.")
        #return jsonify({"mensaje": "credenciales invalidas"}),401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "token": access_token, "role_enum":user.tipo_usuario, "iduser": user.id
    }), 200

@jwt_required()
def obtener_usuario_actual():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email
    }), 200


#@jwt_required()
#def obtener_usuario():
#   user_id = get_jwt_identity()

#    user = User.query.get(user_id)

#   if not user:
#        return jsonify({"mensaje": "Usuario no encontrado"}), 404

#   return jsonify({
#        "id": user.id,
#        "nombre": user.nombre,
#        "email": user.email
#    }), 200

#@jwt_required()
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

    try:
        usuario = User.query.get(user_id)

        if not usuario:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        if usuario.tipo_usuario == "Chofer":
            chofer = Chofer.query.get(user_id)
            if not chofer:
                return jsonify({"mensaje": "Datos de chofer no encontrados"}), 404
            
            return jsonify({
                "id": chofer.id,
                "nombre": usuario.nombre,
                "lastname": chofer.lastname,
                "email": usuario.email,
                "username": chofer.username,
                "licencia": chofer.licencia,
                "imagen_url": chofer.imagen_url,
                "direccion": chofer.direccion,
                "edad": chofer.edad,
                "experienciaLaboral": chofer.experienciaLaboral,
                "telefono": chofer.telefono,
                "status": chofer.status,
                "tipo_usuario": usuario.tipo_usuario
            }), 200

        elif usuario.tipo_usuario == "Administrador":
            administrador = Administrador.query.get(user_id)
            if not administrador:
                return jsonify({"mensaje": "Datos de administrador no encontrados"}), 404
            
            return jsonify({
                "id": administrador.id,
                "nombre": usuario.nombre,
                "lastname": administrador.lastname,
                "email": usuario.email,
                "username": administrador.username,
                "imagen_url": administrador.imagen_url,
                "direccion": administrador.direccion,
                "edad": administrador.edad,
                "experienciaLaboral": administrador.experienciaLaboral,
                "telefono": administrador.telefono,
                "status": administrador.status,
                "tipo_usuario": usuario.tipo_usuario
            }), 200

        return jsonify({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "tipo_usuario": usuario.tipo_usuario
        }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error al obtener el usuario", "error": str(e)}), 500


#@jwt_required()
def actualizar_usuario():
    user_id = get_jwt_identity() 
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404  

    data = request.form  
    file = request.files.get('imagen')  

    nombre = data.get('nombre')
    email = data.get('email')
    status = data.get('status')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    edad = data.get('edad')
    experienciaLaboral = data.get('experienciaLaboral')
    licencia = data.get('licencia')
    username = data.get('username')

    if nombre:
        user.nombre = nombre
    if email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({"mensaje": "El email ya está registrado"}), 400
        user.email = email

    # El tipo de usuario no se puede modificar, así que no se actualiza aquí
    # if tipo_usuario: 
    #     tipos_validos = ["Administrador", "Pasajero", "Chofer"]
    #     if tipo_usuario not in tipos_validos:
    #         return jsonify({"mensaje": f"Tipo de usuario inválido. Debe ser uno de: {', '.join(tipos_validos)}"}), 400
    #     user.tipo_usuario = tipo_usuario

    if status:
        user.status = status
    if telefono:
        user.telefono = telefono
    if direccion:
        user.direccion = direccion
    if edad:
        user.edad = edad
    if experienciaLaboral:
        user.experienciaLaboral = experienciaLaboral
    if licencia:
        user.licencia = licencia
    if username:
        user.username = username

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
        "status": user.status,
        "telefono": user.telefono,
        "direccion": user.direccion,
        "edad": user.edad,
        "experienciaLaboral": user.experienciaLaboral,
        "licencia": user.licencia,
        "username": user.username,
        "imagen_url": user.imagen_url
    }), 200

#@jwt_required()
def eliminar_usuario(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"mensaje": "Usuario eliminado"}), 200
#@jwt_required()
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
    
@jwt_required()
def asignar_terminal_admin(admin_id):
    try:
        # Obtener el ID de la terminal del cuerpo de la solicitud
        data = request.get_json()
        terminal_id = data.get("terminal_id")

        if not terminal_id:
            return jsonify({"mensaje": "El ID de la terminal es obligatorio"}), 400

        # Buscar al administrador por su ID
        administrador = Administrador.query.get(admin_id)

        if not administrador:
            return jsonify({"mensaje": "Administrador no encontrado"}), 404

        # Verificar que la terminal existe
        terminal = Terminal.query.get(terminal_id)

        if not terminal:
            return jsonify({"mensaje": "Terminal no encontrada"}), 404

        # Asignar la terminal al administrador
        administrador.terminal_id = terminal_id
        db.session.commit()

        return jsonify({"mensaje": "Terminal asignada correctamente al administrador"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": "Error al asignar la terminal", "error": str(e)}), 500
    
def obtener_choferes_por_terminal(terminal_id):
    try:
        # Obtener los choferes del terminal
        choferes = Chofer.query.filter_by(terminal_id=terminal_id).all()

        if not choferes:
            return jsonify({"error": "No se encontraron choferes para el terminal especificado"}), 404

        choferes_list = []
        for chofer in choferes:
            respuesta = {
                "id": chofer.id,
                "username": chofer.username,
                "lastname": chofer.lastname,
                "licencia": chofer.licencia,
                "imagen_url": chofer.imagen_url,
                "direccion": chofer.direccion,
                "edad": chofer.edad,
                "experienciaLaboral": chofer.experienciaLaboral,
                "telefono": chofer.telefono,
                "status": chofer.status
            }
            choferes_list.append(respuesta)

        return jsonify(choferes_list), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener los choferes", "detalle": str(e)}), 500
