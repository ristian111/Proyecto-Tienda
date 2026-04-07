from flask import Blueprint
from controllers import ventas_controllers
from security import token_requerido

ventas_bp = Blueprint('ventas_v1', __name__)


@ventas_bp.route('/rapida', methods=['POST'])
@token_requerido
def registrar_venta_rapida():
    datos = ventas_controllers.venta_rapida_registro()
    return datos
