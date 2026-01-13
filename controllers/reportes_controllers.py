from flask import jsonify, request
from services.reportes_services import listar_clientes_con_mas_pedidos, listar_usuarios_con_mas_registro_pedidos

def clientes_con_mas_pedidos():
    limit = request.args.get("limit", default=5, type=int)
    datos = listar_clientes_con_mas_pedidos(limit=limit)
    return jsonify(datos), 200

def usuarios_con_mas_pedidos_registrados():
    limit = request.args.get("limit", default=5, type=int)
    datos = listar_usuarios_con_mas_registro_pedidos(limit=limit)
    return jsonify(datos), 200