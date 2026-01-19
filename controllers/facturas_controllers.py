from flask import jsonify, request
from services import (listar_facturas, registrar_factura, actualizar_factura, eliminar_factura, 
                      obtener_factura_por_uuid, obtener_pedido_por_uuid)

def fac_listado():
    # Devuelve en formato json el listado de facturas junto al codigo http 
    datos = listar_facturas()
    return jsonify(datos), 200

def fac_registro(pedido_uuid):
    
    tipo_venta = request.args.get('tipo', default=False, type=bool)

    pedido_id = obtener_pedido_por_uuid(pedido_uuid)
    if pedido_id:
        pedido = pedido_id["id"]

        try:
            commit = registrar_factura(pedido, tipo_venta, pedido_uuid)
            return jsonify({"mensaje": "Factura registrada",
                            "Factura": commit}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return jsonify({"mensaje": "Error no existe el pedido"}), 500

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
    faltantes = [x for x in requeridos if x not in data]

    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
    numero_factura = data['numero_factura'].strip()
    total          = data['total']
    estado         = data['estado'].strip()
    ref_pedido     = data['ref_pedido'].strip()

    try:
        total = int(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser número entero"}), 400
    
    if not isinstance(numero_factura, str) or len(numero_factura) == 0:
        return jsonify({"mensaje": "'numero_factura' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(estado, str) or len(estado) == 0:
        return jsonify({"mensaje": "'estado' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(ref_pedido, str) or len(ref_pedido) == 0:
        return jsonify({"mensaje": "'ref_pedido' debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if total <= 0:
        return jsonify({"mensaje": "El total no puede ser negativo o igual a cero"}), 400
    
    pedido = obtener_pedido_por_uuid(ref_pedido)

    if not pedido:
        return jsonify({"mensaje": "El pedido no existe"}), 404
    
    pedido_id = pedido['id']

    commit = actualizar_factura(uuid, numero_factura, total, estado, pedido_id)
    if commit:
        return jsonify({"mensaje": "Factura actualizada exitosamente"}), 201
    return jsonify({"mensaje": "Error al actualizar factura"}), 500
