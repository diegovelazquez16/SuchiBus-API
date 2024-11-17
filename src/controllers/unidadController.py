from flask import jsonify, request, send_file
from src.models.unidades import Unidad, db
from src.controllers.driveController import upload_to_drive, download_from_drive  
import tempfile  
import os  
import re
from io import BytesIO



def crear_unidad(data, file):
    if not file:
        return jsonify({"mensaje": "Se requiere un archivo para imagen_url"}), 400

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)
    file_id = upload_to_drive(file_path, file.filename)
    google_drive_url = f"https://drive.google.com/uc?id={file_id}"
    os.remove(file_path)

    nueva_unidad = Unidad(
        numPlaca=data.get("numPlaca"),
        status=data.get("status"),
        modelo=data.get("modelo"),
        marca=data.get("marca"),
        fecha_compra=data.get("fecha_compra"),
        imagen_url=google_drive_url,  
        terminal_id=data.get("terminal_id")
    )

    db.session.add(nueva_unidad)
    db.session.commit()

    return jsonify({"mensaje": "Unidad creada con éxito"}), 201


def obtener_unidades():
    unidades = Unidad.query.all()  
    return jsonify([{
        "id": unidad.id,
        "numPlaca": unidad.numPlaca,
        "status": unidad.status,  
        "modelo": unidad.modelo,
        "marca": unidad.modelo,
        "fecha_compra": unidad.modelo,
        "terminal_id": unidad.terminal_id
    } for unidad in unidades]), 200



def obtener_unidad(id):
    try:
        unidad = Unidad.query.get(id)
        if unidad is None:
            return jsonify({"error": "Unidad no encontrada"}), 404

        respuesta = {
            "id": unidad.id,
            "numPlaca": unidad.numPlaca,
            "status": unidad.status,
            "modelo": unidad.modelo,
            "marca": unidad.marca,
            "fecha_compra": unidad.fecha_compra,
            "terminal_id": unidad.terminal_id,
        }

        if unidad.imagen_url:
            try:
                match = re.search(r'id=([a-zA-Z0-9_-]+)', unidad.imagen_url)
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

def obtener_informacion_unidad(id):
    try:
        unidad = Unidad.query.get(id)
        if unidad is None:
            return jsonify({"error": "Unidad no encontrada"}), 404

        respuesta = {
            "id": unidad.id,
            "numPlaca": unidad.numPlaca,
            "status": unidad.status,
            "modelo": unidad.modelo,
            "marca": unidad.marca,
            "fecha_compra": unidad.fecha_compra,
            "terminal_id": unidad.terminal_id,
            "imagen_url": unidad.imagen_url
        }

        return jsonify(respuesta), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener la información de la unidad", "detalle": str(e)}), 500


def actualizar_unidad(id, data, file=None):
    try:
        unidad = Unidad.query.get(id)
        if unidad is None:
            return jsonify({"error": "Unidad no encontrada"}), 404

        if data:
            unidad.numPlaca = data.get('numPlaca', unidad.numPlaca)
            unidad.status = data.get('status', unidad.status)
            unidad.modelo = data.get('modelo', unidad.modelo)
            unidad.marca = data.get('marca', unidad.marca)
            unidad.fecha_compra = data.get('fecha_compra', unidad.fecha_compra)
            unidad.terminal_id = data.get('terminal_id', unidad.terminal_id)

        if file:
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, file.filename)

            file.save(file_path)
            imagen_id = upload_to_drive(file_path, file.filename)  
            os.remove(file_path)  

            unidad.imagen_url = f"https://drive.google.com/uc?id={imagen_id}"

        db.session.commit()

        response = {
            "id": unidad.id,
            "numPlaca": unidad.numPlaca,
            "status": unidad.status,
            "modelo": unidad.modelo,
            "marca": unidad.marca,
            "fecha_compra": unidad.fecha_compra,
            "terminal_id": unidad.terminal_id
        }

        if unidad.imagen_url:
            response["imagen_url"] = unidad.imagen_url

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Error al actualizar la unidad", "detalle": str(e)}), 500

def eliminar_unidad(unidad_id):
    unidad = Unidad.query.get(unidad_id)

    if not unidad:
        return jsonify({"mensaje": "Unidad no encontrada"}), 404

    db.session.delete(unidad)
    db.session.commit()

    return jsonify({"mensaje": "Unidad eliminada"}), 200



def obtener_unidades_por_terminal(terminal_id):
    unidades = Unidad.query.filter_by(terminal_id=terminal_id).all()
    unidades_list = [{
        "id": unidad.id,
        "numPlaca": unidad.numPlaca,
        "status": unidad.status,
        "modelo": unidad.modelo,
        "marca": unidad.marca,
        "fecha_compra": unidad.fecha_compra,
        "imagen_url": unidad.imagen_url 
    } for unidad in unidades]

    return jsonify(unidades_list), 200
