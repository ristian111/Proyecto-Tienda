from flask import jsonify
from services.reportes_services import listar_clientes_con_mas_pedidos

def clientes_con_mas_pedidos():
    datos = listar_clientes_con_mas_pedidos()
    return jsonify(datos), 200