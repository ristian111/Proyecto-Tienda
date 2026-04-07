from flask import Blueprint
from controllers import estadisticas_controller
from security import token_requerido

estadisticas_bp = Blueprint('estadisticas_bp', __name__)

estadisticas_bp.route('/resumen-hoy', methods=['GET'])(token_requerido(estadisticas_controller.resumen_hoy))
estadisticas_bp.route('/top-productos', methods=['GET'])(token_requerido(estadisticas_controller.top_productos))
estadisticas_bp.route('/ingresos-ganancias', methods=['GET'])(token_requerido(estadisticas_controller.ingresos_ganancias))
estadisticas_bp.route('/horas-pico', methods=['GET'])(token_requerido(estadisticas_controller.horas_pico))
estadisticas_bp.route('/productos-estancados', methods=['GET'])(token_requerido(estadisticas_controller.productos_estancados))
estadisticas_bp.route('/porcentaje-categorias', methods=['GET'])(token_requerido(estadisticas_controller.porcentaje_categorias))
