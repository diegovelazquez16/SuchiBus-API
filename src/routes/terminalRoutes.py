
from flask import Blueprint, request
from src.controllers.terminalController import (
    crear_terminal,
    obtener_terminal,
    obtener_todas_terminales,
    actualizar_terminal,
    eliminar_terminal,
    obtener_unidades_de_terminal,
    obtener_colonias_por_cp
)

terminal_blueprint = Blueprint('terminales', __name__)

@terminal_blueprint.route('/terminales', methods=['POST'])
def ruta_crear_terminal():
    data = request.get_json()
    return crear_terminal(data)

@terminal_blueprint.route('/terminales/<int:id>', methods=['GET'])
def ruta_obtener_terminal(id):
    return obtener_terminal(id)

@terminal_blueprint.route('/terminales', methods=['GET'])
def ruta_obtener_todas_terminales():
    return obtener_todas_terminales()

@terminal_blueprint.route('/terminales/<int:id>', methods=['PUT'])
def ruta_actualizar_terminal(id):
    data = request.get_json()
    return actualizar_terminal(id, data)

@terminal_blueprint.route('/terminales/<int:id>', methods=['DELETE'])
def ruta_eliminar_terminal(id):
    return eliminar_terminal(id)

@terminal_blueprint.route('/terminales/<int:id>/unidades', methods=['GET'])
def ruta_obtener_unidades_de_terminal(id):
    return obtener_unidades_de_terminal(id)

@terminal_blueprint.route('/colonias', methods=['GET'])
def ruta_obtener_colonias():
    return obtener_colonias_por_cp()

