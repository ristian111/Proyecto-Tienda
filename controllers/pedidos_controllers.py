from flask import jsonify, request
from services import pedidos_services, usuarios_services, clientes_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def ped_listado():
    uuid_usuario = request.usuario['uuid']
    datos = pedidos_services.listar_pedidos(uuid_usuario)
    return jsonify(datos), 200

@manejo_errores
def ped_registro():
    # Valida que no existan campos vacios
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["estado", "total", "direccion_entrega", "ref_cliente", "ref_usuario"])

    if validar_requeridos:
        return validar_requeridos

    # Guarda los valores de la petición en variables
    estado            = data['estado']
    total             = data['total']
    direccion_entrega = data['direccion_entrega']
    ref_cliente       = data['ref_cliente']
    ref_usuario       = data['ref_usuario']

    # Valida los campos numericos para verificar que cumplen esta regla
    validar_numeros = controllers.limpieza_numeros({"total": total})

    if validar_numeros:
        return validar_numeros

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    validar_datos = controllers.limpieza_datos(
        {"estado": estado, "direccion_entrega": direccion_entrega, 
         "ref_cliente": ref_cliente, "ref_usuario": ref_usuario})

    if validar_datos:
        return validar_datos
    
    # Revisa si la referencia del cliente existe a través del uuid
    cliente = clientes_services.obtener_cliente_por_uuid(ref_cliente.strip())
    if not cliente:
        return jsonify({"mensaje": "El cliente no existe"}), 404

    uuid_usuario = request.usuario['uuid']
    # Revisa si la referencia del usuario existe a través del uuid
    usuario = usuarios_services.obtener_usuario_por_uuid(uuid_usuario)
    if not usuario:
        return jsonify({"mensaje": "El usuario no existe"}), 404

    # Donde se guarda en las variables para acceder a la id del cliente y del usuario
    cliente_id = cliente['id']
    usuario_id = usuario['id']

    commit = pedidos_services.registrar_pedido(estado.strip(), total, direccion_entrega.strip(), cliente_id, usuario_id, ref_cliente.strip(), uuid_usuario)
    return jsonify({"mensaje": "Pedido registrado exitosamente",
                    "Pedido": commit}), 201

@manejo_errores
def ped_eliminacion(uuid):
    uuid_usuario = request.usuario['uuid']
    # Valida la existencia del inventario a través del uuid 
    pedido = pedidos_services.obtener_pedido_por_uuid(uuid, uuid_usuario)

    if pedido:
        commit = pedidos_services.eliminar_pedido(uuid, uuid_usuario)
        if commit:
            return jsonify({"mensaje": "Pedido eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar pedido"}), 500
    return jsonify({"mensaje": "El pedido no existe"}), 404

@manejo_errores
# Se valida de la misma manera que al registrar
def ped_actualizacion(uuid):
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["estado", "total", "direccion_entrega", "ref_cliente", "ref_usuario"])

    if validar_requeridos:
        return validar_requeridos

    estado            = data['estado']
    total             = data['total']
    direccion_entrega = data['direccion_entrega']
    ref_cliente       = data['ref_cliente']
    ref_usuario       = data['ref_usuario']

    validar_numeros = controllers.limpieza_numeros({"total": total})
    
    if validar_numeros:
        return validar_numeros
    
    validar_datos = controllers.limpieza_datos(
        {"estado": estado, "total": total, "direccion_entrega": direccion_entrega, 
         "ref_cliente": ref_cliente, "ref_usuario": ref_usuario})

    if validar_datos:
        return validar_datos
    
    cliente = clientes_services.obtener_cliente_por_uuid(ref_cliente.strip())
    if not cliente:
        return jsonify({"mensaje": "El cliente no existe"}), 404
    
    uuid_usuario = request.usuario['uuid']
    usuario = usuarios_services.obtener_usuario_por_uuid(uuid_usuario)
    if not usuario:
        return jsonify({"mensaje": "El usuario no existe"}), 404
    
    cliente_id = cliente['id']
    usuario_id = usuario['id']

    pedido = pedidos_services.obtener_pedido_por_uuid(uuid, uuid_usuario)
    if pedido:
            
        commit = pedidos_services.actualizar_pedido(uuid.strip(), estado.strip(), total, direccion_entrega.strip(), cliente_id, usuario_id, ref_cliente.strip(), uuid_usuario)
        return jsonify({"mensaje": "Pedido actualizado exitosamente",
                        "Pedido": commit}), 200

    return jsonify({"mensaje": "El pedido no existe"}), 404

@manejo_errores
def ped_listar_pedidos_pendientes():
    uuid_usuario = request.usuario['uuid']
    datos = pedidos_services.listar_pedidos_pendientes(uuid_usuario)
    return jsonify(datos), 200

@manejo_errores
def ped_listar_detalles(uuid):
    datos = pedidos_services.listar_detalles_pedido(uuid)
    return jsonify(datos), 200

@manejo_errores
def ped_rapida_registro():
    data = request.get_json()

    if not data or 'items' not in data:
        return jsonify({"mensaje": "Se requiere el campo 'items'"}), 400

    items = data['items']

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"mensaje": "La lista de items no puede estar vacía"}), 400

    for i, item in enumerate(items):
        for campo in ['ref_producto', 'cantidad', 'precio_unitario']:
            if campo not in item:
                return jsonify({"mensaje": f"Item {i+1}: falta el campo '{campo}'"}), 400

        if not isinstance(item['cantidad'], (int, float)) or item['cantidad'] <= 0:
            return jsonify({"mensaje": f"Item {i+1}: cantidad debe ser mayor a 0"}), 400

        if not isinstance(item['precio_unitario'], (int, float)) or item['precio_unitario'] <= 0:
            return jsonify({"mensaje": f"Item {i+1}: precio_unitario debe ser mayor a 0"}), 400

    fecha = data.get('fecha')
    uuid_usuario = request.usuario['uuid']

    try:
        resultado = pedidos_services.registrar_pedido_rapido(items, uuid_usuario, fecha)
        return jsonify({
            "mensaje": "Pedido registrado exitosamente",
            "pedido": resultado
        }), 201
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400