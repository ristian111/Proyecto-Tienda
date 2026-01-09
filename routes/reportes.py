from flask import Blueprint
from controllers.reportes_controllers import clientes_con_mas_pedidos

reportes_bp = Blueprint("reportes", __name__)

@reportes_bp.route('/clientes/mas-pedidos', methods=['GET'])
def listar_clientes_con_mas_pedidos():
    datos = clientes_con_mas_pedidos()
    return datos