from flask import jsonify, request
from services.inventarios_services import listar_inventarios, registrar_inventario, actualizar_inventario, eliminar_inventario, obtener_inventario_por_uuid
from services.productos_services import obtener_producto_por_uuid

def inv_listado():
    datos = listar_inventarios()
    return jsonify(datos), 200

def inv_registro():
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

    commit = registrar_inventario(producto_id, cantidad_actual, cantidad_reservada, punto_reorden)
    if commit:
        return jsonify({"mensaje": "Inventario registrado exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar inventario"}), 500
    
def inv_eliminacion(uuid):

    inventario = obtener_inventario_por_uuid(uuid)

    if inventario:
        commit = eliminar_inventario(uuid)
        if commit:
            return jsonify({"mensaje": "Inventario eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar inventario"}), 500
    return jsonify({"mensaje": "El inventario no existe"}), 404

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