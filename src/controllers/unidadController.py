from flask import jsonify, request
from src.models.unidades import Unidad, db

def crear_unidad(data):
    if db.session.query(Unidad).filter_by(numPlaca=data["numPlaca"]).first() is not None:
        return jsonify({"error": "El número de placa ya existe"}), 400

    nueva_unidad = Unidad(
        numPlaca=data["numPlaca"],
        status=data["status"],      
        modelo=data["modelo"],
        marca=data["marca"],
        fecha_compra=["fecha_compra"],
        terminal_id=data["terminal_id"]
    )
    db.session.add(nueva_unidad)
    db.session.commit()

    response_data = {
        "id": nueva_unidad.id,
        "numPlaca": nueva_unidad.numPlaca,
        "status": nueva_unidad.status,
        "modelo": nueva_unidad.modelo,
        "marca": nueva_unidad.modelo,
        "fecha_compra": nueva_unidad.modelo,
        "terminal_id": nueva_unidad.terminal_id
    }

    return jsonify(response_data), 201


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


from flask import jsonify

def obtener_unidad(id):
    unidad = Unidad.query.get(id) 
    if unidad is None:
        return jsonify({"error": "Unidad no encontrada"}), 404 

    
    return jsonify({
        "id": unidad.id,
        "numPlaca": unidad.numPlaca,
        "status": unidad.status,  
        "modelo": unidad.modelo,
        "marca": unidad.modelo,
        "fecha_compra": unidad.modelo,
        "terminal_id": unidad.terminal_id
    }), 200

def actualizar_unidad(id, data):
    unidad = Unidad.query.get(id)
    if unidad is None:
        return jsonify({"error": "Unidad no encontrada"}), 404

    unidad.numPlaca = data.get('numPlaca', unidad.numPlaca)
    unidad.status = data.get('status', unidad.status)  
    unidad.modelo = data.get('modelo', unidad.modelo)
    unidad.marca = data.get('marca', unidad.marca)
    unidad.fecha_compra = data.get('fecha_compra', unidad.fecha_compra)
    unidad.terminal_id = data.get('terminal_id', unidad.terminal_id)

    db.session.commit()  

    return jsonify({
        "id": unidad.id,
        "numPlaca": unidad.numPlaca,
        "status": unidad.status,  
        "modelo": unidad.modelo,
        "marca": unidad.modelo,
        "fecha_compra": unidad.modelo,
        "terminal_id": unidad.terminal_id
    }), 200


def eliminar_unidad(unidad_id):
    unidad = Unidad.query.get(unidad_id)

    if not unidad:
        return jsonify({"mensaje": "Unidad no encontrada"}), 404

    db.session.delete(unidad)
    db.session.commit()

    return jsonify({"mensaje": "Unidad eliminada"}), 200
