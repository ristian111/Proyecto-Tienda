from flask import Blueprint
from controllers.pedidos_controllers import ped_listado, ped_registro, ped_actualizacion, ped_eliminacion, ped_listar_pedidos_pendientes
pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/', methods=['GET'])
def listar():
    datos = ped_listado()
    return datos

@pedidos_bp.route('/', methods=['POST'])
def registrar():
    datos = ped_registro()
    return datos

@pedidos_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = ped_actualizacion(uuid)
    return datos

@pedidos_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = ped_eliminacion(uuid)
    return datos

@pedidos_bp.route('/pendientes', methods=['GET'])
def listar_pedidos_pendientes():
    datos = ped_listar_pedidos_pendientes()
    return datos