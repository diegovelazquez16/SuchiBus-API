from flask import jsonify, request
from src.models.terminal import Terminal, db
from flask_jwt_extended import jwt_required
from flask import jsonify, request
import json
import requests


SEPOMEX_API_URL = "https://api.tau.com.mx/dipomex/v1/codigo_postal"
SEPOMEX_API_KEY = "942458d38dbd17909612270eb547be864622de08"

@jwt_required()
def crear_terminal(data):
    nombre = data.get('nombre')
    cp = data.get('cp')
    calle = data.get('calle')
    num = data.get('num')
    horarioApertura = data.get('horarioApertura')
    horarioCierre = data.get('horarioCierre')
    telefono = data.get('telefono')
    administradorid = data.get('administradorid')
    ruta_id= data.get('ruta_id')

    print(f"Recibido administrador_id: {administradorid}")  # Verificar el valor

    if not all([nombre, cp, calle, num, horarioApertura, horarioCierre, telefono, ruta_id]):
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    headers = {"APIKEY": SEPOMEX_API_KEY}
    params = {"cp": cp}

    try:
        response = requests.get(SEPOMEX_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            sepomex_data = response.json()

            if sepomex_data.get("error", True):
                return jsonify({"mensaje": "La API de Sepomex devolvió un error", "detalles": sepomex_data.get("message", "Error desconocido")}), 400

            codigo_postal_data = sepomex_data.get("codigo_postal")
            estado = codigo_postal_data.get("estado")
            municipio = codigo_postal_data.get("municipio")
            colonias = codigo_postal_data.get("colonias")

            direccion = {
                "cp": cp,
                "estado": estado,
                "municipio": municipio,
                "colonia": colonias[0] if colonias else None,
                "calle": calle,
                "num": num
            }

            nueva_terminal = Terminal(
                nombre=nombre,
                direccion=json.dumps(direccion),
                horarioApertura=horarioApertura,
                horarioCierre=horarioCierre,
                telefono=telefono,
                administrador_id= administradorid,
                ruta_id= ruta_id
            )

            db.session.add(nueva_terminal)
            db.session.commit()

            return jsonify({
                "mensaje": "Terminal creada exitosamente",
                "id": nueva_terminal.id,
                "nombre": nueva_terminal.nombre,
                "direccion": direccion
            }), 201

        else:
            return jsonify({"mensaje": "Error al consultar la API de Sepomex", "detalles": response.json()}), 400

    except requests.RequestException as e:
        return jsonify({"mensaje": "Error al conectar con la API de Sepomex", "detalles": str(e)}), 500
 
@jwt_required()    
def obtener_colonias_por_cp():
    cp = request.args.get('cp') 
    if not cp:
        return jsonify({"mensaje": "El código postal es necesario"}), 400

    headers = {"APIKEY": SEPOMEX_API_KEY}
    params = {"cp": cp}

    try:
        response = requests.get(SEPOMEX_API_URL, headers=headers, params=params)

        print(f"Respuesta de Sepomex: {response.text}")

        if response.status_code == 200:
            sepomex_data = response.json()

            if sepomex_data.get("error", True):
                return jsonify({"mensaje": "La API de Sepomex devolvió un error", "detalles": sepomex_data.get("message", "Error desconocido")}), 400

            codigo_postal_data = sepomex_data.get("codigo_postal")
            if not codigo_postal_data:
                return jsonify({"mensaje": "La API de Sepomex no devolvió datos completos"}), 400

            estado = codigo_postal_data.get("estado")
            municipio = codigo_postal_data.get("municipio")
            colonias = codigo_postal_data.get("colonias")

            if not estado or not municipio or not colonias:
                return jsonify({"mensaje": "Datos incompletos en la respuesta de la API de Sepomex"}), 400

            return jsonify({
                "cp": cp,
                "estado": estado,
                "municipio": municipio,
                "colonias": colonias
            }), 200

        else:
            return jsonify({"mensaje": "Error al consultar la API de Sepomex", "detalles": response.json()}), 400

    except requests.RequestException as e:
        return jsonify({"mensaje": "Error al conectar con la API de Sepomex", "detalles": str(e)}), 500


@jwt_required()
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
        'administrador_id': terminal.administrador_id,
        "ruta_id": terminal.ruta_id

    }), 200

@jwt_required()
def obtener_todas_terminales():
    
    terminales = Terminal.query.all()
    terminales_list = [{
        "id": terminal.id,
        "nombre": terminal.nombre,
        "direccion": terminal.direccion,  
        "horarioApertura": terminal.horarioApertura,
        "horarioCierre": terminal.horarioCierre,
        "telefono": terminal.telefono,
        'administrador_id': terminal.administrador_id,
        "ruta_id": terminal.ruta_id

    } for terminal in terminales]

    return jsonify(terminales_list), 200
@jwt_required()
def actualizar_terminal(id_terminal, data):
    nombre = data.get('nombre')
    cp = data.get('cp')
    calle = data.get('calle')
    num = data.get('num')
    horarioApertura = data.get('horarioApertura')
    horarioCierre = data.get('horarioCierre')
    telefono = data.get('telefono')
    administradorid = data.get('administradorid')

    terminal = Terminal.query.get(id_terminal)
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    if not any([nombre, cp, calle, num, horarioApertura, horarioCierre, telefono]):
        return jsonify({"mensaje": "No se proporcionaron datos para actualizar"}), 400

    direccion = None

    if cp:
        headers = {"APIKEY": SEPOMEX_API_KEY}
        params = {"cp": cp}

        try:
            response = requests.get(SEPOMEX_API_URL, headers=headers, params=params)
            if response.status_code == 200:
                sepomex_data = response.json()
                if sepomex_data.get("error", True):
                    return jsonify({"mensaje": "La API de Sepomex devolvió un error", "detalles": sepomex_data.get("message", "Error desconocido")}), 400

                codigo_postal_data = sepomex_data.get("codigo_postal")
                estado = codigo_postal_data.get("estado")
                municipio = codigo_postal_data.get("municipio")
                colonias = codigo_postal_data.get("colonias")

                direccion = {
                    "cp": cp,
                    "estado": estado,
                    "municipio": municipio,
                    "colonia": colonias[0] if colonias else None,
                    "calle": calle or terminal.direccion.get('calle'),
                    "num": num or terminal.direccion.get('num')
                }

        except requests.RequestException as e:
            return jsonify({"mensaje": "Error al conectar con la API de Sepomex", "detalles": str(e)}), 500

    # Actualizar campos
    if nombre:
        terminal.nombre = nombre
    if direccion:
        terminal.direccion = json.dumps(direccion)
    if horarioApertura:
        terminal.horarioApertura = horarioApertura
    if horarioCierre:
        terminal.horarioCierre = horarioCierre
    if telefono:
        terminal.telefono = telefono
    if administradorid:
        terminal.administrador_id = administradorid

    # Guardar cambios en la base de datos
    try:
        db.session.commit()
        return jsonify({
            "mensaje": "Terminal actualizada exitosamente",
            "id": terminal.id,
            "nombre": terminal.nombre,
            "direccion": json.loads(terminal.direccion)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": "Error al actualizar la terminal", "detalles": str(e)}), 500




@jwt_required()
def eliminar_terminal(id):
    terminal = Terminal.query.get(id)
    if not terminal:
        return jsonify({"mensaje": "Terminal no encontrada"}), 404

    db.session.delete(terminal)
    db.session.commit()

    return jsonify({"mensaje": "Terminal eliminada"}), 200

#@jwt_required()
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


