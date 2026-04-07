from flask import Blueprint
from controllers import productos_controllers
from security import token_requerido
productos_bp = Blueprint('productos_v1', __name__)

@productos_bp.route('/', methods=['GET'])
@token_requerido
def listar():
    datos = productos_controllers.prod_listado()
    return datos

@productos_bp.route('/', methods=['POST'])
@token_requerido
def registrar():
    datos = productos_controllers.prod_registro()
    return datos

@productos_bp.route('/<string:uuid>', methods=['DELETE'])
@token_requerido
def eliminar(uuid):
    datos = productos_controllers.prod_eliminacion(uuid)
    return datos

@productos_bp.route('/<string:uuid>', methods=['PUT'])
@token_requerido
def actualizar(uuid):
    datos = productos_controllers.prod_actualizacion(uuid)
    return datos