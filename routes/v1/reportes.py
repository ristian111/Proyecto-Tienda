from flask import Blueprint
from controllers import reportes_controllers
reportes_bp = Blueprint("reportes_v1", __name__)

@reportes_bp.route('/clientes/mas-pedidos', methods=['GET'])
def listar_clientes_con_mas_pedidos():
    datos = reportes_controllers.rep_clientes_con_mas_pedidos()
    return datos

@reportes_bp.route('/usuarios/mas-pedidos-registrados', methods=['GET'])
def listar_usuarios_con_mas_pedidos_registrados():
    datos = reportes_controllers.rep_usuarios_con_mas_pedidos_registrados()
    return datos

@reportes_bp.route('/productos/mas-vendidos', methods=['GET'])
def listar_productos_mas_vendidos():
    datos = reportes_controllers.rep_productos_mas_vendidos()
    return datos

@reportes_bp.route('/pedidos/por-fecha', methods=['GET'])
def listar_pedidos_por_fecha():
    datos = reportes_controllers.rep_pedidos_por_fecha()
    return datos

@reportes_bp.route('/productos/mas-ganancias', methods=['GET'])
def listar_productos_con_mas_ganancias():
    datos = reportes_controllers.rep_productos_mas_ganancias()
    return datos

@reportes_bp.route('/facturas/ingresos', methods=['GET'])
def listar_ingresos_ventas():
    datos = reportes_controllers.rep_ingresos_generados()
    return datos