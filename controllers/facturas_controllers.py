from flask import jsonify, request
from services import facturas_services, pedidos_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def fac_listado():
    # Devuelve en formato json el listado de facturas junto al codigo http 
    datos = facturas_services.listar_facturas()
    return jsonify(datos), 200

@manejo_errores
def fac_registro(pedido_uuid):
    tipo_venta = request.args.get('tipo', default=None)

    if tipo_venta is None:
        tipo_venta = False
    
    tipo_venta = True

    pedido_id = pedidos_services.obtener_pedido_por_uuid(pedido_uuid)
    if pedido_id:
        pedido = pedido_id["id"]
        try:
            commit = facturas_services.registrar_factura(pedido, tipo_venta, pedido_uuid)
            return jsonify({"mensaje": "Factura registrada",
                            "Factura": commit}), 201
        except Exception as e:
            return jsonify({"mensaje": str(e)}), 500
    
    return jsonify({"mensaje": "Error no existe el pedido"}), 404

@manejo_errores
def fac_eliminacion(uuid):
    # Valida la existencia de la factura a través del uuid 
    factura = facturas_services.obtener_factura_por_uuid(uuid)

    if factura:
        commit = facturas_services.eliminar_factura(uuid)
        if commit:
            return jsonify({"mensaje": "Factura eliminada exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar la factura"}), 500
    return jsonify({"mensaje": "La factura no existe"}), 404

@manejo_errores
# Se valida de la misma manera que al registrar
def fac_actualizacion(uuid):
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["numero_factura", "total", "estado", "ref_pedido"])
    
    if validar_requeridos:
        return validar_requeridos
    
    numero_factura = data['numero_factura']
    total          = data['total']
    estado         = data['estado']
    ref_pedido     = data['ref_pedido']

    try:
        total = int(total)
    except ValueError:
        return jsonify({"mensaje": "El campo total debe ser número entero"}), 400
    
    validar_datos = controllers.limpieza_datos({"numero_factura": numero_factura, "estado": estado, "ref_pedido": ref_pedido})

    if validar_datos:
        return validar_datos
    
    if total <= 0:
        return jsonify({"mensaje": "El total no puede ser negativo o igual a cero"}), 400
    
    pedido = pedidos_services.obtener_pedido_por_uuid(ref_pedido.strip())

    if not pedido:
        return jsonify({"mensaje": "El pedido no existe"}), 404
    
    pedido_id = pedido['id']

    commit = facturas_services.actualizar_factura(uuid.strip(), numero_factura.strip(), total, estado.strip(), pedido_id)
    if commit:
        return jsonify({"mensaje": "Factura actualizada exitosamente"}), 200
    return jsonify({"mensaje": "Error al actualizar factura"}), 500
