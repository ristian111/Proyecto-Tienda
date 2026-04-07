from flask import Blueprint
from controllers import detalle_pedido_controllers
from security import token_requerido
detalle_pedido_bp = Blueprint("detalles_v1", __name__)

@detalle_pedido_bp.route("/pedidos", methods=['GET'])
@token_requerido
def listado():
    datos = detalle_pedido_controllers.det_pedido_listado()
    return datos

@detalle_pedido_bp.route("/pedidos", methods=['POST'])
@token_requerido
def registro():
    datos = detalle_pedido_controllers.det_pedido_registro()
    return datos

@detalle_pedido_bp.route("/pedidos/<string:uuid>", methods=['DELETE'])
@token_requerido
def eliminacion(uuid):
    datos = detalle_pedido_controllers.det_pedido_eliminacion(uuid)
    return datos

@detalle_pedido_bp.route("/pedidos/<string:uuid>", methods=['PUT'])
@token_requerido
def actualizacion(uuid):
    datos = detalle_pedido_controllers.det_pedido_actualizacion(uuid)
    return datos
