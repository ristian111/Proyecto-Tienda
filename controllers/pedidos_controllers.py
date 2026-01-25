from flask import jsonify, request
from services import pedidos_services, usuarios_services, clientes_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def ped_listado():
    # Devuelve en formato json el listado de pedidos junto al codigo http 
    datos = pedidos_services.listar_pedidos()
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
    try:
        total = float(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser un número entero"}), 400

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

    # Revisa si la referencia del usuario existe a través del uuid
    usuario = usuarios_services.obtener_usuario_por_uuid(ref_usuario.strip())
    if not usuario:
        return jsonify({"mensaje": "El usuario no existe"}), 404

    # Donde se guarda en las variables para acceder a la id del cliente y del usuario
    cliente_id = cliente['id']
    usuario_id = usuario['id']

    try:
        commit = pedidos_services.registrar_pedido(estado.strip(), total, direccion_entrega.strip(), cliente_id, usuario_id, ref_cliente.strip(), ref_usuario.strip())
        return jsonify({"mensaje": "Pedido registrado exitosamente",
                        "Pedido": commit}), 201
    except RuntimeError as e:
        return jsonify({"mensaje": str(e)}), 500

@manejo_errores
def ped_eliminacion(uuid):
    # Valida la existencia del inventario a través del uuid 
    pedido = pedidos_services.obtener_pedido_por_uuid(uuid)

    if pedido:
        commit = pedidos_services.eliminar_pedido(uuid)
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

    try:
        total = float(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser un número entero"}), 400
    
    validar_datos = controllers.limpieza_datos(
        {"estado": estado, "total": total, "direccion_entrega": direccion_entrega, 
         "ref_cliente": ref_cliente, "ref_usuario": ref_usuario})

    if validar_datos:
        return validar_datos
    
    cliente = clientes_services.obtener_cliente_por_uuid(ref_cliente.strip())
    if not cliente:
        return jsonify({"mensaje": "El cliente no existe"}), 404
    
    usuario = usuarios_services.obtener_usuario_por_uuid(ref_usuario.strip())
    if not usuario:
        return jsonify({"mensaje": "El usuario no existe"}), 404
    
    cliente_id = cliente['id']
    usuario_id = usuario['id']

    pedido = pedidos_services.obtener_pedido_por_uuid(uuid)
    if pedido:
        try:
            commit = pedidos_services.actualizar_pedido(uuid.strip(), estado.strip(), total, direccion_entrega.strip(), cliente_id, usuario_id, ref_cliente.strip(), ref_usuario.strip())
            return jsonify({"mensaje": "Pedido actualizado exitosamente",
                            "Pedido": commit}), 200
        except Exception:
            return jsonify({"mensaje": "Error al actualizar pedido"}), 500
    return jsonify({"mensaje": "El pedido no existe"}), 404

@manejo_errores
def ped_listar_pedidos_pendientes():
    datos = pedidos_services.listar_pedidos_pendientes()
    return jsonify(datos), 200