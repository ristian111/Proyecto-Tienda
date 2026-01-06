from flask import jsonify, request
from services.clientes_services import listar_clientes, registrar_clientes, actualizar_cliente, eliminar_cliente, obtener_cliente_por_uuid

def cli_listado():
    # Devuelve en formato json el listado de clientes junto al codigo http 
    datos = listar_clientes()
    return jsonify(datos), 200

def cli_registro():
    # Valida que no existan campos vacios 
    data = request.get_json()

    requeridos = ["nombre", "telefono", "direccion"]
    faltantes = [x for x in requeridos if x not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
    # Guarda los valores de la petición en variables
    nombre    = data['nombre']
    telefono  = data['telefono']
    direccion = data['direccion']

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    if not isinstance(nombre, str) or nombre.strip() == "":
        return jsonify({"mensaje": "El nombre debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(telefono, str) or telefono.strip() == "":
        return jsonify({"mensaje": "El telefono debe ser una cadena de texto o no puede estar vacio"}), 400
    
    # Valida a través de operadores de comparación para asegurar los datos
    if len(telefono.strip()) < 10:
        return jsonify({"mensaje": "El telefono debe tener al menos 10 caracteres"}), 400

    if not isinstance(direccion, str) or direccion.strip() == "":
        return jsonify({"mensaje": "La direccion debe ser una cadena de texto o no puede estar vacia"}), 400
    
    commit = registrar_clientes(nombre, telefono, direccion)
    if commit:
        return jsonify({"mensaje": "Cliente registrado exitosamente"}), 201
    return jsonify({"mensaje": "Error al registrar cliente"}), 500

def cli_eliminacion(uuid):
    # Valida la existencia del cliente a través del uuid 
    cliente = obtener_cliente_por_uuid(uuid)
    if cliente:
        commit = eliminar_cliente(uuid)
        if commit:
            return jsonify({"mensaje": "Cliente eliminado exitosamente"}), 200
        
        return jsonify({"mensaje": "Error al eliminar cliente"}), 500
    return jsonify({"mensaje": "El cliente no existe"}), 404

# Se valida de la misma manera que al registrar
def cli_actualizacion(uuid):
    data = request.get_json()

    requeridos = ["nombre", "telefono", "direccion"]
    faltantes = [x for x in requeridos if x not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
    nombre    = data['nombre']
    telefono  = data['telefono']
    direccion = data['direccion']

    if not isinstance(nombre, str) or nombre.strip() == "":
        return jsonify({"mensaje": "El nombre debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(telefono, str) or telefono.strip() == "":
        return jsonify({"mensaje": "El telefono debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if len(telefono.strip()) < 10:
        return jsonify({"mensaje": "El telefono debe tener al menos 10 caracteres"}), 400

    if not isinstance(direccion, str) or direccion.strip() == "":
        return jsonify({"mensaje": "La direccion debe ser una cadena de texto o no puede estar vacia"}), 400
    
    commit = actualizar_cliente(uuid, nombre, telefono, direccion)
    if commit:
        return jsonify({"mensaje": "Cliente actualizado exitosamente"}), 200
    return jsonify({"mensaje": "Error al actualizar cliente"}), 500