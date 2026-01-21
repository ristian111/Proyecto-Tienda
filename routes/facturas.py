from flask import blueprints
from controllers import facturas_controllers
facturas_bp = blueprints.Blueprint('facturas', __name__)

@facturas_bp.route('/', methods=['GET'])
def listar():
    datos = facturas_controllers.fac_listado()
    return datos

@facturas_bp.route('/<string:pedido_uuid>', methods=['POST'])
def registrar(pedido_uuid):
    datos = facturas_controllers.fac_registro(pedido_uuid)
    return datos

@facturas_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = facturas_controllers.fac_eliminacion(uuid)
    return datos

@facturas_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):    
    datos = facturas_controllers.fac_actualizacion(uuid)
    return datos