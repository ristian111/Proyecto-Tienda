from flask import jsonify, request
from services.facturas_services import listar_facturas, registrar_factura, actualizar_factura, eliminar_factura, obtener_factura_por_uuid
from services.pedidos_services import obtener_pedido_por_uuid

def fac_listado():
    # Devuelve en formato json el listado de facturas junto al codigo http 
    datos = listar_facturas()
    return jsonify(datos), 200

def fac_registro():
    # Valida que no existan campos vacios 
    data = request.get_json()

    requeridos = ["numero_factura", "total", "estado", "ref_pedido"]
    faltantes = [x for x in requeridos if requeridos not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400

    # Guarda los valores de la petición en variables
    numero_factura = data['numero_factura']
    total          = data['total']
    estado         = data['estado']
    ref_pedido     = data['ref_pedido']

    # Valida los campos numericos para verificar que cumplen esta regla
    try:
        total = int(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser número entero"}), 400
    
    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    if not isinstance(numero_factura, str) or len(numero_factura.strip()) == 0:
        return jsonify({"mensaje": "'numero_factura' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(estado, str) or len(estado.strip()) == 0:
        return jsonify({"mensaje": "'estado' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_pedido, str) or len(ref_pedido.strip()) == 0:
        return jsonify({"mensaje": "'ref_pedido' debe ser una cadena de texto o no puede estar vacio"}), 400

    # Valida a través de operadores de comparación para asegurar los datos
    if total <= 0:
        return jsonify({"mensaje": "El total no puede ser negativo"}), 400
    
    # Revisa si la referencia del pedido existe a través del uuid
    pedido = obtener_pedido_por_uuid(ref_pedido)

    if not pedido:
        return jsonify({"mensaje": "El pedido no existe"}), 404
    # Donde se guarda en una variable para acceder a la id del pedido
    pedido_id = pedido['id']

    commit = registrar_factura(numero_factura, total, estado, pedido_id)
    if commit:
        return jsonify({"mensaje": "Factura registrada exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar factura"}), 500

def fac_eliminacion(uuid):
    # Valida la existencia de la factura a través del uuid 
    factura = obtener_factura_por_uuid(uuid)

    if factura:
        commit = eliminar_factura(uuid)
        if commit:
            return jsonify({"mensaje": "Factura eliminada exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar la factura"}), 500
    return jsonify({"mensaje": "La factura no existe"}), 404

# Se valida de la misma manera que al registrar
def fac_actualizacion(uuid):
    data = request.get_json()

    requeridos = ["numero_factura", "total", "estado", "ref_pedido"]
    faltantes = [x for x in requeridos if requeridos not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
    numero_factura = data['numero_factura']
    total          = data['total']
    estado         = data['estado']
    ref_pedido     = data['ref_pedido']

    try:
        total = int(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser número entero"}), 400
    
    if not isinstance(numero_factura, str) or len(numero_factura.strip()) == 0:
        return jsonify({"mensaje": "'numero_factura' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(estado, str) or len(estado.strip()) == 0:
        return jsonify({"mensaje": "'estado' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_pedido, str) or len(ref_pedido.strip()) == 0:
        return jsonify({"mensaje": "'ref_pedido' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if total <= 0:
        return jsonify({"mensaje": "El total no puede ser negativo o igual a cero"}), 400
    
    pedido = obtener_pedido_por_uuid(ref_pedido)

    if not pedido:
        return jsonify({"mensaje": "El pedido no existe"}), 404
    
    pedido_id = pedido['id']

    commit = actualizar_factura(uuid, numero_factura, total, estado, pedido_id)
    if commit:
        return jsonify({"mensaje": "Factura actualizada exitosamente"}), 200
    return jsonify({"mensaje": "Error al actualizar factura"}), 500
