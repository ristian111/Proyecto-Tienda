from flask import jsonify, request
from services import compras_services
from decoradores import manejo_errores

@manejo_errores
def compra_rapida_registro():
    data = request.get_json()

    if not data or 'items' not in data:
        return jsonify({"mensaje": "Se requiere el campo 'items'"}), 400

    items = data['items']

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"mensaje": "La lista de items no puede estar vacía"}), 400

    # Validar items
    for i, item in enumerate(items):
        if 'ref_producto' not in item:
            return jsonify({"mensaje": f"Item {i+1}: falta el campo 'ref_producto'"}), 400
        if 'cantidad' not in item or float(item['cantidad']) <= 0:
            return jsonify({"mensaje": f"Item {i+1}: cantidad inválida"}), 400
        if 'costo' not in item or float(item['costo']) < 0:
            return jsonify({"mensaje": f"Item {i+1}: costo inválido"}), 400

    fecha = data.get('fecha')
    uuid_usuario = request.usuario['uuid']

    try:
        resultado = compras_services.registrar_compra_rapida(items, uuid_usuario, fecha)
        return jsonify({
            "mensaje": "Compra registrada exitosamente",
            "compra": resultado
        }), 201
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
