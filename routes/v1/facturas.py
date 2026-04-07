from flask import blueprints
from controllers import facturas_controllers
from security import token_requerido
facturas_bp = blueprints.Blueprint('facturas_v1', __name__)

@facturas_bp.route('/', methods=['GET'])
@token_requerido
def listar():
    datos = facturas_controllers.fac_listado()
    return datos

@facturas_bp.route('/<string:pedido_uuid>', methods=['POST'])
@token_requerido
def registrar(pedido_uuid):
    datos = facturas_controllers.fac_registro(pedido_uuid)
    return datos

@facturas_bp.route('/<string:uuid>', methods=['DELETE'])
@token_requerido
def eliminar(uuid):
    datos = facturas_controllers.fac_eliminacion(uuid)
    return datos

@facturas_bp.route('/<string:uuid>', methods=['PUT'])
@token_requerido
def actualizar(uuid):    
    datos = facturas_controllers.fac_actualizacion(uuid)
    return datos