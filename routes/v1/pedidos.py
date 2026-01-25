from flask import Blueprint
from controllers import pedidos_controllers
pedidos_bp = Blueprint('pedidos_v1', __name__)

@pedidos_bp.route('/', methods=['GET'])
def listar():
    datos = pedidos_controllers.ped_listado()
    return datos

@pedidos_bp.route('/', methods=['POST'])
def registrar():
    datos = pedidos_controllers.ped_registro()
    return datos

@pedidos_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = pedidos_controllers.ped_actualizacion(uuid)
    return datos

@pedidos_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = pedidos_controllers.ped_eliminacion(uuid)
    return datos

@pedidos_bp.route('/pendientes', methods=['GET'])
def listar_pedidos_pendientes():
    datos = pedidos_controllers.ped_listar_pedidos_pendientes()
    return datos