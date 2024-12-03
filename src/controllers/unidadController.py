from flask import jsonify, request, send_file, json
from src.models.unidades import Unidad, db
from src.controllers.driveController import upload_to_drive, download_from_drive  
import tempfile  
import os  
import re
from io import BytesIO
from flask import send_file

def crear_unidad(data, file):
    if 'file' not in request.files:
        return jsonify({"mensaje": "Se requiere un archivo para imagen_url"}), 400
    
    file = request.files['file']
    if not file:
        return jsonify({"mensaje": "Se requiere un archivo para imagen_url"}), 400
    print("Archivo recibido:", file)
    
    # Se cargan los datos de la unidad
    data = json.loads(request.form['data'])
    
    # Guardar temporalmente el archivo
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    
    try:
        file.save(file_path)
        print(f"Archivo guardado temporalmente en: {file_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return jsonify({"mensaje": "Error al guardar el archivo"}), 500
    
    # Subir el archivo a Google Drive
    try:
        file_id = upload_to_drive(file_path, file.filename)
        # Solo guardamos el file_id, no la URL completa
    except Exception as e:
        print(f"Error al subir el archivo a Google Drive: {e}")
        return jsonify({"mensaje": "Error al subir el archivo a Google Drive"}), 500
    
    # Crear la nueva unidad en la base de datos
    try:
        nueva_unidad = Unidad(
            numPlaca=data.get("numPlaca"),
            status=data.get("status"),
            modelo=data.get("modelo"),
            marca=data.get("marca"),
            fecha_compra=data.get("fecha_compra"),
            num_asientos=data.get("num_asientos"),
            actual_cupo=data.get("actual_cupo"),
            imagen_url=file_id,  # Guardamos solo el file_id
            terminal_id=data.get("terminal_id"),
            imagen_archivo=file.filename  # Guardamos el nombre del archivo
        )
        
        db.session.add(nueva_unidad)
        db.session.commit()
        print("Unidad creada con éxito:", nueva_unidad, file_id)
    except Exception as e:
        print(f"Error al crear la unidad: {e}")
        return jsonify({"mensaje": "Error al crear la unidad"}), 500
    
    return jsonify({"mensaje": "Unidad creada con éxito"}), 201


def obtener_unidades():
    try:
        unidades = Unidad.query.all() 
        unidades_respuesta = []

        for unidad in unidades:
            respuesta = {
                "id": unidad.id,
                "numPlaca": unidad.numPlaca,
                "status": unidad.status,
                "modelo": unidad.modelo,
                "marca": unidad.marca,
                "fecha_compra": unidad.fecha_compra,
                "num_asientos": unidad.num_asientos,
                "actual_cupo": unidad.actual_cupo,
                "terminal_id": unidad.terminal_id,
                "imagen_archivo": unidad.imagen_archivo,
                "imagen_url": unidad.imagen_url,
                
            }
        return jsonify(unidades_respuesta), 200

    except Exception as e:
        return jsonify({"error": "Error procesando la solicitud", "detalle": str(e)}), 500


def obtener_unidad(id):
    try:
        # Obtén la unidad de la base de datos
        unidad = Unidad.query.get(id)
        if unidad is None:
            return jsonify({"error": "Unidad no encontrada"}), 404

        # Construye la respuesta básica
        respuesta = {
            "id": unidad.id,
            "numPlaca": unidad.numPlaca,
            "status": unidad.status,
            "modelo": unidad.modelo,
            "marca": unidad.marca,
            "fecha_compra": unidad.fecha_compra,
            "num_asientos": unidad.num_asientos,
            "actual_cupo": unidad.actual_cupo,
            "terminal_id": unidad.terminal_id,
            "imagen_url": unidad.imagen_url,
            "imagen_archivo": unidad.imagen_archivo,
        }

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
            "num_asientos": unidad.num_asientos,
            "actual_cupo": unidad.actual_cupo,
            "terminal_id": unidad.terminal_id,
            "imagen_url": unidad.imagen_url,
            "imagen_archivo": unidad.imagen_archivo
        }

    except Exception as e:
        return jsonify({"error": "Error al obtener la información de la unidad", "detalle": str(e)}), 500


def actualizar_unidad(id, data, file=None):
    try:
        unidad = Unidad.query.get(id)
        if not unidad:
            return jsonify({"mensaje": "Unidad no encontrada"}), 404

        if data:
            unidad.numPlaca = data.get("numPlaca", unidad.numPlaca)
            unidad.status = data.get("status", unidad.status)
            unidad.modelo = data.get("modelo", unidad.modelo)
            unidad.marca = data.get("marca", unidad.marca)
            unidad.fecha_compra = data.get("fecha_compra", unidad.fecha_compra)
            unidad.num_asientos = data.get("num_asientos", unidad.num_asientos)
            unidad.actual_cupo = data.get("actual_cupo", unidad.actual_cupo)
            unidad.terminal_id = data.get("terminal_id", unidad.terminal_id)

        if file:
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, file.filename)

            try:
                file.save(file_path)
                imagen_id = upload_to_drive(file_path, file.filename)
                os.remove(file_path)  

                unidad.imagen_url = f"https://drive.google.com/uc?id={imagen_id}"
                unidad.imagen_archivo = file.filename
            except Exception as e:
                print(f"Error al manejar la imagen: {e}")
                return jsonify({"mensaje": "Error al procesar la imagen"}), 500

        db.session.commit()

        return jsonify({
            "mensaje": "Unidad actualizada con éxito",
            "unidad": {
                "id": unidad.id,
                "numPlaca": unidad.numPlaca,
                "status": unidad.status,
                "modelo": unidad.modelo,
                "marca": unidad.marca,
                "fecha_compra": unidad.fecha_compra,
                "num_asientos": unidad.num_asientos,
                "actual_cupo": unidad.actual_cupo,
                "terminal_id": unidad.terminal_id,
                "imagen_url": unidad.imagen_url
            }
        }), 200

    except Exception as e:
        return jsonify({"mensaje": "Error al actualizar la unidad", "detalle": str(e)}), 500

def eliminar_unidad(unidad_id):
    unidad = Unidad.query.get(unidad_id)

    if not unidad:
        return jsonify({"mensaje": "Unidad no encontrada"}), 404

    db.session.delete(unidad)
    db.session.commit()

    return jsonify({"mensaje": "Unidad eliminada"}), 200

def obtener_unidades_por_terminal(terminal_id):
    try:
        # Obtener las unidades del terminal
        unidades = Unidad.query.filter_by(terminal_id=terminal_id).all()

        if not unidades:
            return jsonify({"error": "No se encontraron unidades para el terminal especificado"}), 404

        unidades_list = []
        for unidad in unidades:
            respuesta = {
                "id": unidad.id,
                "numPlaca": unidad.numPlaca,
                "status": unidad.status,
                "modelo": unidad.modelo,
                "marca": unidad.marca,
                "fecha_compra": unidad.fecha_compra,
                "num_asientos": unidad.num_asientos,
                "hora_salida": unidad.hora_salida,
                "hora_llegada": unidad.hora_llegada,
                "actual_cupo": unidad.actual_cupo,
                "imagen_url": unidad.imagen_url,  # Aquí dejas la URL o la referencia
                "imagen_archivo": unidad.imagen_archivo  # Este es el nombre o referencia del archivo
            }
            unidades_list.append(respuesta)

        return jsonify(unidades_list), 200

    except Exception as e:
        return jsonify({"error": "Error al obtener las unidades", "detalle": str(e)}), 500

def actualizar_horarios_unidad(id, data):
    try:
        unidad = Unidad.query.get(id)
        if not unidad:
            return jsonify({"error": "Unidad no encontrada"}), 404

        horario_entrada = data.get("horario_entrada")
        horario_salida = data.get("horario_salida")

        if not horario_entrada or not horario_salida:
            return jsonify({"error": "Se requieren ambos horarios"}), 400

        unidad.horario_entrada = horario_entrada
        unidad.horario_salida = horario_salida

        db.session.commit()

        response = {
            "id": unidad.id,
            "numPlaca": unidad.numPlaca,
            "horario_entrada": unidad.horario_entrada,
            "horario_salida": unidad.horario_salida
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Error al actualizar los horarios", "detalle": str(e)}), 500