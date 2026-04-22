from flask import jsonify, request
from services import ventas_services
from decoradores import manejo_errores


@manejo_errores
def venta_rapida_registro():
    data = request.get_json()

    if not data or 'items' not in data:
        return jsonify({"mensaje": "Se requiere el campo 'items'"}), 400

    items = data['items']

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"mensaje": "La lista de items no puede estar vacía"}), 400

    # Validar cada item
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
        resultado = ventas_services.registrar_venta_rapida(items, uuid_usuario, fecha)
        return jsonify({
            "mensaje": "Venta registrada exitosamente",
            "venta": resultado
        }), 201
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
