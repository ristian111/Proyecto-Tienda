from flask import jsonify, request
from services import (listar_detalles_pedidos, registrar_detalle_pedido, actualizar_detalle_pedido, 
                      eliminar_detalle_pedido, obtener_detalle_pedido_por_uuid, obtener_pedido_por_uuid, 
                      obtener_producto_por_uuid)

def det_pedido_listado():
    # Devuelve en formato json el listado del detalle_pedido junto al codigo http 
    datos = listar_detalles_pedidos()
    return jsonify(datos), 200

def det_pedido_registro():
    # Valida que no existan campos vacios 
    datos = request.get_json()

    requeridos = ["cantidad", "precio_unitario", "ref_pedido", "ref_producto"]
    faltantes  = [x for x in requeridos if x not in datos]

    if faltantes:
        return jsonify({"mensaje": f"faltan los campos {faltantes}"}), 400
    
    # Guarda los valores de la petición en variables
    cantidad        = datos['cantidad']
    precio_unitario = datos['precio_unitario']
    ref_pedido      = datos['ref_pedido'].strip()
    ref_producto    = datos['ref_producto'].strip()

    # Valida los campos numericos para verificar que cumplen esta regla 
    try:
        cantidad        = int(cantidad)
        precio_unitario = float(precio_unitario)
    except ValueError:
        return jsonify({"mensaje": "El campo cantidad y precio_unitario deben ser números enteros"}), 400

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    if not isinstance(ref_pedido, str) or len(ref_pedido) == 0:
        return jsonify({"mensaje": "'ref_pedido' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_producto, str) or len(ref_producto) == 0:
        return jsonify({"mensaje": "'ref_producto' debe ser una cadena de texto o no puede estar vacio"}), 400

    # Valida a través de operadores de comparación para asegurar los datos
    if cantidad <= 0:
        return jsonify({"mensaje": "La cantidad no puede ser negativa o igual a cero"}), 400
    
    if precio_unitario <= 0:
        return jsonify({"mensaje": "El precio_unitario no puede ser negativo o igual a cero"}), 400

    # Revisa si la referencia del pedido existe a través del uuid
    pedido = obtener_pedido_por_uuid(ref_pedido)

    if not pedido:
        return jsonify({"mensaje": "El pedido no existe"}), 404

    # Revisa si la referencia del producto existe a través del uuid
    producto = obtener_producto_por_uuid(ref_producto)

    if not producto:
        return jsonify({"mensaje": "El producto no existe"}), 404
    
    # Donde se guarda en una variable para acceder a la id del pedido y del producto
    pedido_id   = pedido['id']
    producto_id = producto['id']

    commit = registrar_detalle_pedido(cantidad, precio_unitario, pedido_id, producto_id)

    if commit:
        return jsonify({"mensaje": "detalle_pedido registrado exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar detalle_pedido"}), 500

def det_pedido_eliminacion(uuid):
    # Valida la existencia del detalle_pedido a través del uuid 
    detalle_pedido = obtener_detalle_pedido_por_uuid(uuid)

    if detalle_pedido:
        commit = eliminar_detalle_pedido(uuid)

        if commit:
            return jsonify({"mensaje": "detalle_pedido eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar el detalle_pedido"}), 500
    return jsonify({"mensaje": "El detalle_pedido no existe"}), 404

def det_pedido_actualizacion(uuid):

    datos = request.get_json()

    requeridos = ["cantidad", "precio_unitario", "ref_pedido", "ref_producto"]
    faltantes  = [x for x in requeridos if x not in datos]

    if faltantes:
        return jsonify({"mensaje": f"faltan los campos {faltantes}"}), 400

    cantidad        = datos['cantidad']
    precio_unitario = datos['precio_unitario']
    ref_pedido      = datos['ref_pedido'].strip()
    ref_producto    = datos['ref_producto'].strip()

    try:
        cantidad        = int(cantidad)
        precio_unitario = float(precio_unitario)
    except ValueError:
        return jsonify({"mensaje": "El campo cantidad y precio_unitario deben ser números enteros"}), 400

    if not isinstance(ref_pedido, str) or len(ref_pedido) == 0:
        return jsonify({"mensaje": "'ref_pedido' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_producto, str) or len(ref_producto) == 0:
        return jsonify({"mensaje": "'ref_producto' debe ser una cadena de texto o no puede estar vacio"}), 400

    if cantidad <= 0:
        return jsonify({"mensaje": "La cantidad no puede ser negativa o igual a cero"}), 400
    
    if precio_unitario <= 0:
        return jsonify({"mensaje": "El precio_unitario no puede ser negativo o igual a cero"}), 400

    pedido = obtener_pedido_por_uuid(ref_pedido)

    if not pedido:
        return jsonify({"mensaje": "El pedido no existe"}), 404

    producto = obtener_producto_por_uuid(ref_producto)

    if not producto:
        return jsonify({"mensaje": "El producto no existe"}), 404
    
    pedido_id   = pedido['id']
    producto_id = producto['id']

    commit = actualizar_detalle_pedido(uuid, cantidad, precio_unitario, pedido_id, producto_id)

    if commit:
        return jsonify({"mensaje": "detalle_pedido actualizado exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al actualizar detalle_pedido"}), 500