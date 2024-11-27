from flask import jsonify, request
from src.models.terminal import Terminal, db
from flask_jwt_extended import jwt_required
import json

def crear_terminal(data):
    nombre = data.get('nombre')
    ciudad = data.get('ciudad')
    colonia = data.get('colonia')
    calle = data.get('calle')
    num = data.get('num')
    horarioApertura = data.get('horarioApertura')
    horarioCierre = data.get('horarioCierre')
    telefono = data.get('telefono')
    ruta_id = data.get('ruta_id')

    if not all([nombre, ciudad, colonia, calle, num, horarioApertura, horarioCierre, telefono, ruta_id]):
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    direccion = {
        "ciudad": ciudad,
        "colonia": colonia,
        "calle": calle,
        "num": num
    }

    nueva_terminal = Terminal(
        nombre=nombre,
        direccion=direccion,
        horarioApertura=horarioApertura,
        horarioCierre=horarioCierre,
        telefono=telefono,
        ruta_id = ruta_id
    )

    db.session.add(nueva_terminal)
    db.session.commit()

    return jsonify({
        "mensaje": "Terminal creada exitosamente",
        "id": nueva_terminal.id,
        "nombre": nueva_terminal.nombre
    }), 201

def obtener_terminal(id):
    terminal = Terminal.query.get(id)
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    direccion = terminal.get_direccion()

    return jsonify({
        "id": terminal.id,
        "nombre": terminal.nombre,
        "direccion": direccion,
        "horarioApertura": terminal.horarioApertura,
        "horarioCierre": terminal.horarioCierre,
        "telefono": terminal.telefono,
        "ruta_id" : terminal.ruta_id
    }), 200


def obtener_todas_terminales():
    terminales = Terminal.query.all()
    terminales_list = [{
        "id": terminal.id,
        "nombre": terminal.nombre,
        "direccion": terminal.direccion,  
        "horarioApertura": terminal.horarioApertura,
        "horarioCierre": terminal.horarioCierre,
        "telefono": terminal.telefono,
        "ruta_id": terminal.ruta_id
    } for terminal in terminales]

    return jsonify(terminales_list), 200





def actualizar_terminal(id, data):
    terminal = Terminal.query.get(id)
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    terminal.nombre = data.get('nombre', terminal.nombre)
    terminal.horarioApertura = data.get('horarioApertura', terminal.horarioApertura)
    terminal.horarioCierre = data.get('horarioCierre', terminal.horarioCierre)
    terminal.telefono = data.get('telefono', terminal.telefono)

    nueva_direccion = data.get('direccion', {})
    if isinstance(nueva_direccion, dict):
        direccion_actual = terminal.get_direccion()  

        direccion_actual.update(nueva_direccion)

        terminal.direccion = json.dumps(direccion_actual)

    db.session.commit()

    return jsonify({"mensaje": "Terminal actualizada exitosamente"}), 200

def eliminar_terminal(id):
    terminal = Terminal.query.get(id)
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    db.session.delete(terminal)
    db.session.commit()

    return jsonify({"mensaje": "Terminal eliminada"}), 200
def obtener_unidades_de_terminal(id):
    # Obtener la terminal con el ID proporcionado
    terminal = Terminal.query.get(id)
    
    # Verificar si la terminal existe
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    # Obtener las unidades asociadas a la terminal
    unidades = [{
        "id": unidad.id,
        "numPlaca": unidad.numPlaca,
        "status": unidad.status,
        "modelo": unidad.modelo,
        "marca": unidad.marca,
        "fecha_Compra": unidad.fecha_Compra
    } for unidad in terminal.unidades]

    # Retornar las unidades en la respuesta JSON
    return jsonify({
        "terminal_id": terminal.id,
        "nombre": terminal.nombre,
        "unidades": unidades
    }), 200