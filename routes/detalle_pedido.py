from flask import Blueprint
from controllers import detalle_pedido_controllers
detalle_pedido_bp = Blueprint("detalles", __name__)

@detalle_pedido_bp.route("/pedidos", methods=['GET'])
def listado():
    datos = detalle_pedido_controllers.det_pedido_listado()
    return datos

@detalle_pedido_bp.route("/pedidos", methods=['POST'])
def registro():
    datos = detalle_pedido_controllers.det_pedido_registro()
    return datos

@detalle_pedido_bp.route("/pedidos/<string:uuid>", methods=['DELETE'])
def eliminacion(uuid):
    datos = detalle_pedido_controllers.det_pedido_eliminacion(uuid)
    return datos

@detalle_pedido_bp.route("/pedidos/<string:uuid>", methods=['PUT'])
def actualizacion(uuid):
    datos = detalle_pedido_controllers.det_pedido_actualizacion(uuid)
    return datos
