from flask import jsonify, request
from services import (listar_pedidos, registrar_pedido, actualizar_pedido, eliminar_pedido, 
                      obtener_pedido_por_uuid, listar_pedidos_pendientes, obtener_cliente_por_uuid, 
                      obtener_usuario_por_uuid)

def ped_listado():
    # Devuelve en formato json el listado de pedidos junto al codigo http 
    datos = listar_pedidos()
    return jsonify(datos), 200

def ped_registro():
    # Valida que no existan campos vacios
    data = request.get_json()

    requeridos = ["estado", "total", "direccion_entrega", "ref_cliente", "ref_usuario"]
    faltantes = [x for x in requeridos if x not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400

    # Guarda los valores de la petición en variables
    estado            = data['estado'].strip()
    total             = data['total']
    direccion_entrega = data['direccion_entrega'].strip()
    ref_cliente       = data['ref_cliente'].strip()
    ref_usuario       = data['ref_usuario'].strip()

    # Valida los campos numericos para verificar que cumplen esta regla
    try:
        total = float(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser un número entero"}), 400

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    if not isinstance(estado, str) or len(estado) == 0:
        return jsonify({"mensaje": "'estado' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(direccion_entrega, str) or len(direccion_entrega) == 0:
        return jsonify({"mensaje": "'direccion_entrega' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_cliente, str) or len(ref_cliente) == 0:
        return jsonify({"mensaje": "'ref_cliente' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_usuario, str) or len(ref_usuario) == 0:
        return jsonify({"mensaje": "'ref_usuario' debe ser una cadena de texto o no puede estar vacio"}), 400

    # Revisa si la referencia del cliente existe a través del uuid
    cliente = obtener_cliente_por_uuid(ref_cliente)
    if not cliente:
        return jsonify({"mensaje": "El cliente no existe"}), 404

    # Revisa si la referencia del usuario existe a través del uuid
    usuario = obtener_usuario_por_uuid(ref_usuario)
    if not usuario:
        return jsonify({"mensaje": "El usuario no existe"}), 404

    # Donde se guarda en las variables para acceder a la id del cliente y del usuario
    cliente_id = cliente['id']
    usuario_id = usuario['id']

    commit = registrar_pedido(estado, total, direccion_entrega, cliente_id, usuario_id)
    if commit:
        return jsonify({"mensaje": "Pedido registrado exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar pedido"}), 500

def ped_eliminacion(uuid):
    # Valida la existencia del inventario a través del uuid 
    pedido = obtener_pedido_por_uuid(uuid)

    if pedido:
        commit = eliminar_pedido(uuid)
        if commit:
            return jsonify({"mensaje": "Pedido eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar pedido"}), 500
    return jsonify({"mensaje": "El pedido no existe"}), 404

# Se valida de la misma manera que al registrar
def ped_actualizacion(uuid):
    data = request.get_json()

    requeridos = ["estado", "total", "direccion_entrega", "ref_cliente", "ref_usuario"]
    faltantes = [x for x in requeridos if x not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400

    estado            = data['estado'].strip()
    total             = data['total']
    direccion_entrega = data['direccion_entrega'].strip()
    ref_cliente       = data['ref_cliente'].strip()
    ref_usuario       = data['ref_usuario'].strip()

    try:
        total = float(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser un número entero"}), 400
    
    if not isinstance(estado, str) or len(estado) == 0:
        return jsonify({"mensaje": "'estado' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(direccion_entrega, str) or len(direccion_entrega) == 0:
        return jsonify({"mensaje": "'direccion_entrega' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_cliente, str) or len(ref_cliente) == 0:
        return jsonify({"mensaje": "'ref_cliente' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_usuario, str) or len(ref_usuario) == 0:
        return jsonify({"mensaje": "'ref_usuario' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    cliente = obtener_cliente_por_uuid(ref_cliente)
    if not cliente:
        return jsonify({"mensaje": "El cliente no existe"}), 404
    
    usuario = obtener_usuario_por_uuid(ref_usuario)
    if not usuario:
        return jsonify({"mensaje": "El usuario no existe"}), 404
    
    cliente_id = cliente['id']
    usuario_id = usuario['id']

    commit = actualizar_pedido(uuid, estado, total, direccion_entrega, cliente_id, usuario_id)
    if commit:
        return jsonify({"mensaje": "Pedido actualizado exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al actualizar pedido"}), 500

def ped_listar_pedidos_pendientes():
    datos = listar_pedidos_pendientes()
    return jsonify(datos), 200