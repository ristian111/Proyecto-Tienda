from flask import Blueprint
from controllers.productos_controllers import prod_listado, prod_actualizacion, prod_eliminacion, prod_registro
productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
def listar():
    datos = prod_listado()
    return datos

@productos_bp.route('/', methods=['POST'])
def registrar():
    datos = prod_registro()
    return datos

@productos_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = prod_eliminacion(uuid)
    return datos

@productos_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = prod_actualizacion(uuid)
    return datos