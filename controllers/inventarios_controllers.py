from flask import jsonify, request
from services.inventarios_services import listar_inventarios, registrar_inventario, actualizar_inventario, eliminar_inventario, obtener_inventario_por_uuid, listar_productos_stock_bajo, listar_stock_producto, listar_movimiento_inventario
from services.productos_services import obtener_producto_por_uuid

def inv_listado():
    # Devuelve en formato json el listado de inventarios junto al codigo http 
    datos = listar_inventarios()
    return jsonify(datos), 200

def inv_listado_movimiento_inventario():
    datos = listar_movimiento_inventario()
    return jsonify(datos), 200

def inv_registro():
    # Valida que no existan campos vacios 
    data = request.get_json()

    requeridos = ["ref_producto", "cantidad_actual", "cantidad_reservada", "punto_reorden"]
    faltantes = [x for x in requeridos if x not in data]
    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
    # Guarda los valores de la petición en variables
    producto_uuid      = data['ref_producto']
    cantidad_actual    = data['cantidad_actual']
    cantidad_reservada = data['cantidad_reservada']
    punto_reorden      = data['punto_reorden']

    # Valida los campos numericos para verificar que cumplen esta regla
    try:
        cantidad_actual    = int(cantidad_actual)
        cantidad_reservada = int(cantidad_reservada)
        punto_reorden      = int(punto_reorden)
    except ValueError:
        return jsonify({"mensaje": "Los campos cantidad_actual, cantidad_reservada y punto_reorden deben ser números enteros"}), 400

    # Valida a través de operadores de comparación para asegurar los datos
    if cantidad_actual < 0:
        return jsonify({"mensaje": "cantidad_actual no puede ser negativa"}), 400
    
    if cantidad_reservada < 0:
        return jsonify({"mensaje": "cantidad_reservada no puede ser negativa"}), 400

    if punto_reorden < 0:
        return jsonify({"mensaje": "punto_reorden no puede ser negativo"}), 400
    
    if cantidad_reservada > cantidad_actual:
        return jsonify({"mensaje": "cantidad_reservada no puede ser mayor que cantidad_actual"}), 400
    
    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    if not isinstance(producto_uuid, str) or len(producto_uuid.strip()) == 0:
        return jsonify({"mensaje": "ref_producto debe ser una cadena de texto o no puede estar vacio"}), 400

    # Revisa si la referencia del producto existe a través del uuid
    producto = obtener_producto_por_uuid(producto_uuid)
    if not producto:
        return jsonify({"mensaje": "El producto no existe"}), 404

    # Donde se guarda en una variable para acceder a la id del producto
    producto_id = producto['id']

    commit = registrar_inventario(producto_id, cantidad_actual, cantidad_reservada, punto_reorden)
    if commit:
        return jsonify({"mensaje": "Inventario registrado exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar inventario"}), 500
    
def inv_eliminacion(uuid):
    # Valida la existencia del inventario a través del uuid 
    inventario = obtener_inventario_por_uuid(uuid)

    if inventario:
        commit = eliminar_inventario(uuid)
        if commit:
            return jsonify({"mensaje": "Inventario eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar inventario"}), 500
    return jsonify({"mensaje": "El inventario no existe"}), 404

# Se valida de la misma manera que al registrar
def inv_actualizacion(uuid):
    data = request.get_json()

    requeridos = ["ref_producto", "cantidad_actual", "cantidad_reservada", "punto_reorden"]
    faltantes = [x for x in requeridos if x not in data]
    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
    producto_uuid      = data['ref_producto']
    cantidad_actual    = data['cantidad_actual']
    cantidad_reservada = data['cantidad_reservada']
    punto_reorden      = data['punto_reorden']
    
    try:
        cantidad_actual    = int(cantidad_actual)
        cantidad_reservada = int(cantidad_reservada)
        punto_reorden      = int(punto_reorden)
    except ValueError:
        return jsonify({"mensaje": "Los campos cantidad_actual, cantidad_reservada y punto_reorden deben ser números enteros"}), 400

    if cantidad_actual < 0:
        return jsonify({"mensaje": "cantidad_actual no puede ser negativa"}), 400
    
    if cantidad_reservada < 0:
        return jsonify({"mensaje": "cantidad_reservada no puede ser negativa"}), 400

    if punto_reorden < 0:
        return jsonify({"mensaje": "punto_reorden no puede ser negativo"}), 400
    
    if cantidad_reservada > cantidad_actual:
        return jsonify({"mensaje": "cantidad_reservada no puede ser mayor que cantidad_actual"}), 400
    
    if not isinstance(producto_uuid, str) or len(producto_uuid.strip()) == 0:
        return jsonify({"mensaje": "ref_producto debe ser una cadena de texto o no puede estar vacio"}), 400
    
    producto = obtener_producto_por_uuid(producto_uuid)
    if not producto:
        return jsonify({"mensaje": "El producto no existe"}), 404

    producto_id = producto['id']

    commit = actualizar_inventario(uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden)
    if commit:
        return jsonify({"mensaje": "Inventario actualizado exitosamente"}), 200
    return jsonify({"mensaje": "Error al actualizar inventario"}), 500

def inv_productos_stock_bajo():

    limite = request.args.get("limit", default=1, type=int)

    commit = listar_productos_stock_bajo(limite)

    if commit:
        return jsonify({"mensaje": "Producto encontrado exitosamente",
                        "Stock producto": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar producto"}), 500

def inv_stock_producto(producto):

    commit = listar_stock_producto(producto)
        
    if commit:
        return jsonify({"mensaje": "Producto encontrado exitosamente",
                        "Stock producto": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar producto"}), 500