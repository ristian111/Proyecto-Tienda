from flask import Blueprint
from controllers import (rep_clientes_con_mas_pedidos, rep_usuarios_con_mas_pedidos_registrados, 
                         rep_productos_mas_vendidos, rep_pedidos_por_fecha, rep_productos_mas_ganancias, 
                         rep_ingresos_generados)

reportes_bp = Blueprint("reportes", __name__)

@reportes_bp.route('/clientes/mas-pedidos', methods=['GET'])
def listar_clientes_con_mas_pedidos():
    datos = rep_clientes_con_mas_pedidos()
    return datos

@reportes_bp.route('/usuarios/mas-pedidos-registrados', methods=['GET'])
def listar_usuarios_con_mas_pedidos_registrados():
    datos = rep_usuarios_con_mas_pedidos_registrados()
    return datos

@reportes_bp.route('/productos/mas-vendidos', methods=['GET'])
def listar_productos_mas_vendidos():
    datos = rep_productos_mas_vendidos()
    return datos

@reportes_bp.route('/pedidos/por-fecha', methods=['GET'])
def listar_pedidos_por_fecha():
    datos = rep_pedidos_por_fecha()
    return datos

@reportes_bp.route('/productos/mas-ganancias', methods=['GET'])
def listar_productos_con_mas_ganancias():
    datos = rep_productos_mas_ganancias()
    return datos

@reportes_bp.route('/facturas/ingresos', methods=['GET'])
def listar_ingresos_ventas():
    datos = rep_ingresos_generados()
    return datos