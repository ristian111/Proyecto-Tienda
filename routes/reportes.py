from flask import Blueprint
from controllers.reportes_controllers import clientes_con_mas_pedidos, usuarios_con_mas_pedidos_registrados

reportes_bp = Blueprint("reportes", __name__)

@reportes_bp.route('/clientes/mas-pedidos', methods=['GET'])
def listar_clientes_con_mas_pedidos():
    datos = clientes_con_mas_pedidos()
    return datos

@reportes_bp.route('/usuarios/mas-pedidos-registrados', methods=['GET'])
def listar_usuarios_con_mas_pedidos_registrados():
    datos = usuarios_con_mas_pedidos_registrados()
    return datos