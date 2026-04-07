from flask import Blueprint
from controllers import pedidos_controllers
from security import token_requerido
pedidos_bp = Blueprint('pedidos_v1', __name__)

@pedidos_bp.route('/', methods=['GET'])
@token_requerido
def listar():
    datos = pedidos_controllers.ped_listado()
    return datos

@pedidos_bp.route('/', methods=['POST'])
@token_requerido
def registrar():
    datos = pedidos_controllers.ped_registro()
    return datos

@pedidos_bp.route('/<string:uuid>', methods=['PUT'])
@token_requerido
def actualizar(uuid):
    datos = pedidos_controllers.ped_actualizacion(uuid)
    return datos

@pedidos_bp.route('/<string:uuid>', methods=['DELETE'])
@token_requerido
def eliminar(uuid):
    datos = pedidos_controllers.ped_eliminacion(uuid)
    return datos

@pedidos_bp.route('/pendientes', methods=['GET'])
@token_requerido
def listar_pedidos_pendientes():
    datos = pedidos_controllers.ped_listar_pedidos_pendientes()
    return datos