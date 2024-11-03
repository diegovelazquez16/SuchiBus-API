from flask import jsonify, request
from src.models.terminal import Terminal, db
from flask_jwt_extended import jwt_required

def crear_terminal(data):
    nombre = data.get('nombre')
    ciudad = data.get('ciudad')
    colonia = data.get('colonia')
    calle = data.get('calle')
    num = data.get('num')
    horario = data.get('horario')

    if not all([nombre, ciudad, colonia, calle, num, horario]):
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    nueva_terminal = Terminal(nombre=nombre, ciudad=ciudad, colonia=colonia, calle=calle, num=num, horario=horario)
    db.session.add(nueva_terminal)
    db.session.commit()

    return jsonify({
        "mensaje": "Terminal creada exitosamente",
        "id": nueva_terminal.id,
        "nombre": nueva_terminal.nombre
    }), 201

@jwt_required()
def obtener_terminal(id):
    terminal = Terminal.query.get(id)
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    return jsonify({
        "id": terminal.id,
        "nombre": terminal.nombre,
        "ciudad": terminal.ciudad,
        "colonia": terminal.colonia,
        "calle": terminal.calle,
        "num": terminal.num,
        "horario": terminal.horario
    }), 200

@jwt_required()
def obtener_todas_terminales():
    terminales = Terminal.query.all()
    terminales_list = [{
        "id": terminal.id,
        "nombre": terminal.nombre,
        "ciudad": terminal.ciudad,
        "colonia": terminal.colonia,
        "calle": terminal.calle,
        "num": terminal.num,
        "horario": terminal.horario
    } for terminal in terminales]

    return jsonify(terminales_list), 200

@jwt_required()
def actualizar_terminal(id, data):
    terminal = Terminal.query.get(id)
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    terminal.nombre = data.get('nombre', terminal.nombre)
    terminal.ciudad = data.get('ciudad', terminal.ciudad)
    terminal.colonia = data.get('colonia', terminal.colonia)
    terminal.calle = data.get('calle', terminal.calle)
    terminal.num = data.get('num', terminal.num)
    terminal.horario = data.get('horario', terminal.horario)

    db.session.commit()

    return jsonify({"mensaje": "Terminal actualizada exitosamente"}), 200

@jwt_required()
def eliminar_terminal(id):
    terminal = Terminal.query.get(id)
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    db.session.delete(terminal)
    db.session.commit()

    return jsonify({"mensaje": "Terminal eliminada"}), 200
