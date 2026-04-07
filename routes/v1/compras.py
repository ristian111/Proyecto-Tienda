from flask import Blueprint
from controllers import compras_controllers as controlador
from security import token_requerido

compras_bp = Blueprint('compras', __name__)

@compras_bp.route('/rapida', methods=['POST'])
@token_requerido
def registro_compra_rapida():
    return controlador.compra_rapida_registro()
