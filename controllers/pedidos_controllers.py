from flask import jsonify, request
from services.pedidos_services import listar_pedidos, registrar_pedido, actualizar_pedido, eliminar_pedido, obtener_pedido_por_uuid
from services.clientes_services import obtener_cliente_por_uuid
from services.usuarios_services import obtener_usuario_por_uuid

def ped_listado():
    datos = listar_pedidos()
    return jsonify(datos), 200

def ped_registro():
    data = request.get_json()

    requeridos = ["estado", "total", "direccion_entrega", "ref_cliente", "ref_usuario"]
    faltantes = [x for x in requeridos if x not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400

    estado            = data['estado']
    total             = data['total']
    direccion_entrega = data['direccion_entrega']
    ref_cliente       = data['ref_cliente']
    ref_usuario       = data['ref_usuario']

    try:
        total = float(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser un número entero"}), 400
    
    if not isinstance(estado, str) or len(estado.strip()) == 0:
        return jsonify({"mensaje": "'estado' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(direccion_entrega, str) or len(direccion_entrega.strip()) == 0:
        return jsonify({"mensaje": "'direccion_entrega' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_cliente, str) or len(ref_cliente.strip()) == 0:
        return jsonify({"mensaje": "'ref_cliente' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_usuario, str) or len(ref_usuario.strip()) == 0:
        return jsonify({"mensaje": "'ref_usuario' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    cliente = obtener_cliente_por_uuid(ref_cliente)
    if not cliente:
        return jsonify({"mensaje": "El cliente no existe"}), 404
    
    usuario = obtener_usuario_por_uuid(ref_usuario)
    if not usuario:
        return jsonify({"mensaje": "El usuario no existe"}), 404
    
    cliente_id = cliente['id']
    usuario_id = usuario['id']

    commit = registrar_pedido(estado, total, direccion_entrega, cliente_id, usuario_id)
    if commit:
        return jsonify({"mensaje": "Pedido registrado exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar pedido"}), 500

def ped_eliminacion(uuid):
    
    pedido = obtener_pedido_por_uuid(uuid)

    if pedido:
        commit = eliminar_pedido(uuid)
        if commit:
            return jsonify({"mensaje": "Pedido eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar pedido"}), 500
    return jsonify({"mensaje": "El pedido no existe"}), 404

def ped_actualizacion(uuid):
    data = request.get_json()

    requeridos = ["estado", "total", "direccion_entrega", "ref_cliente", "ref_usuario"]
    faltantes = [x for x in requeridos if x not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400

    estado            = data['estado']
    total             = data['total']
    direccion_entrega = data['direccion_entrega']
    ref_cliente       = data['ref_cliente']
    ref_usuario       = data['ref_usuario']

    try:
        total = float(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser un número entero"}), 400
    
    if not isinstance(estado, str) or len(estado.strip()) == 0:
        return jsonify({"mensaje": "'estado' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(direccion_entrega, str) or len(direccion_entrega.strip()) == 0:
        return jsonify({"mensaje": "'direccion_entrega' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_cliente, str) or len(ref_cliente.strip()) == 0:
        return jsonify({"mensaje": "'ref_cliente' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_usuario, str) or len(ref_usuario.strip()) == 0:
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