# routes/unidadRoutes.py
from flask import Blueprint, request
from src.controllers.unidadController import (
    crear_unidad,
    obtener_unidad,
    obtener_unidades,
    actualizar_unidad,
    eliminar_unidad
)

unidad_blueprint = Blueprint('unidades', __name__)

@unidad_blueprint.route('/unidades', methods=['POST'])
def ruta_crear_unidad():
    data = request.get_json()
    return crear_unidad(data)

@unidad_blueprint.route('/unidades/<int:id>', methods=['GET'])
def ruta_obtener_unidad(id):
    return obtener_unidad(id)

@unidad_blueprint.route('/unidades', methods=['GET'])
def ruta_obtener_todas_unidades():
    return obtener_unidades()

@unidad_blueprint.route('/unidades/<int:id>', methods=['PUT'])
def ruta_actualizar_unidad(id):
    data = request.get_json()
    return actualizar_unidad(id, data)

@unidad_blueprint.route('/unidades/<int:id>', methods=['DELETE'])
def ruta_eliminar_unidad(id):
    return eliminar_unidad(id)
