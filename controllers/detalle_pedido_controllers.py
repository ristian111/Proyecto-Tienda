from flask import jsonify, request
from services import detalle_pedido_services, pedidos_services, productos_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def det_pedido_listado():
    # Devuelve en formato json el listado del detalle_pedido junto al codigo http 
    datos = detalle_pedido_services.listar_detalles_pedidos()
    return jsonify(datos), 200

@manejo_errores
def det_pedido_registro():
    # Valida que no existan campos vacios 
    datos = request.get_json()

    validar_requeridos = controllers.validar_campos(datos, ["cantidad", "precio_unitario", "ref_pedido", "ref_producto"])
    
    if validar_requeridos:
        return validar_requeridos
    
    # Guarda los valores de la petición en variables
    cantidad        = datos['cantidad']
    precio_unitario = datos['precio_unitario']
    ref_pedido      = datos['ref_pedido']
    ref_producto    = datos['ref_producto']

    # Valida los campos numericos para verificar que cumplen esta regla 
    try:
        cantidad        = int(cantidad)
        precio_unitario = float(precio_unitario)
    except ValueError:
        return jsonify({"mensaje": "El campo cantidad y precio_unitario deben ser números enteros"}), 400

    validar_datos = controllers.limpieza_datos({"ref_pedido": ref_pedido, "ref_producto": ref_producto})
    
    if validar_datos:
        return validar_datos

    # Revisa si la referencia del pedido existe a través del uuid
    pedido = pedidos_services.obtener_pedido_por_uuid(ref_pedido.strip())

    if not pedido:
        return jsonify({"mensaje": "El pedido no existe"}), 404

    # Revisa si la referencia del producto existe a través del uuid
    producto = productos_services.obtener_producto_por_uuid(ref_producto.strip())

    if not producto:
        return jsonify({"mensaje": "El producto no existe"}), 404
    
    # Donde se guarda en una variable para acceder a la id del pedido y del producto
    pedido_id   = pedido['id']
    producto_id = producto['id']

    try:
        commit = detalle_pedido_services.registrar_detalle_pedido(cantidad, precio_unitario, pedido_id, producto_id, ref_pedido.strip(), ref_producto.strip())
        return jsonify({"mensaje": "detalle_pedido registrado exitosamente",
                        "Detalle_pedido": commit}), 201
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"mensaje": str(e)}), 500

@manejo_errores
def det_pedido_eliminacion(uuid):
    # Valida la existencia del detalle_pedido a través del uuid 
    detalle_pedido = detalle_pedido_services.obtener_detalle_pedido_por_uuid(uuid)

    if detalle_pedido:
        commit = detalle_pedido_services.eliminar_detalle_pedido(uuid)

        if commit:
            return jsonify({"mensaje": "detalle_pedido eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar el detalle_pedido"}), 500
    return jsonify({"mensaje": "El detalle_pedido no existe"}), 404

@manejo_errores
def det_pedido_actualizacion(uuid):

    datos = request.get_json()

    validar_requeridos = controllers.validar_campos(datos, ["cantidad", "precio_unitario", "ref_pedido", "ref_producto"])
    
    if validar_requeridos:
        return validar_requeridos
    
    cantidad        = datos['cantidad']
    precio_unitario = datos['precio_unitario']
    ref_pedido      = datos['ref_pedido']
    ref_producto    = datos['ref_producto']

    try:
        cantidad        = int(cantidad)
        precio_unitario = float(precio_unitario)
    except ValueError:
        return jsonify({"mensaje": "El campo cantidad y precio_unitario deben ser números enteros"}), 400

    validar_datos = controllers.limpieza_datos({"ref_pedido": ref_pedido, "ref_producto": ref_producto})
    
    if validar_datos:
        return validar_datos

    pedido = pedidos_services.obtener_pedido_por_uuid(ref_pedido.strip())

    if not pedido:
        return jsonify({"mensaje": "El pedido no existe"}), 404

    producto = productos_services.obtener_producto_por_uuid(ref_producto.strip())

    if not producto:
        return jsonify({"mensaje": "El producto no existe"}), 404
    
    pedido_id   = pedido['id']
    producto_id = producto['id']

    detalle_pedido = detalle_pedido_services.obtener_detalle_pedido_por_uuid(uuid)
    if detalle_pedido:
        try:
            commit = detalle_pedido_services.actualizar_detalle_pedido(uuid, cantidad, precio_unitario, pedido_id, producto_id, ref_pedido.strip(), ref_producto.strip())
            return jsonify({"mensaje": "detalle_pedido actualizado exitosamente",
                            "Detalle_pedido": commit}), 200
        except ValueError as e:
            return jsonify({"mensaje": str(e)}), 400
        except Exception:
            return jsonify({"mensaje": "Error al actualizar detalle_pedido"}), 500
    return jsonify({"mensaje": "El detalle_pedido no existe"}), 404