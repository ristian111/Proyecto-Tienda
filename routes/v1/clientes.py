from flask import Blueprint
from controllers import clientes_controllers
from security import token_requerido

clientes_bp = Blueprint('clientes_v1', __name__)

@clientes_bp.route('/', methods=['GET'])
@token_requerido
def listar():
    datos = clientes_controllers.cli_listado()
    return datos

@clientes_bp.route('/', methods=['POST'])
@token_requerido
def registrar():
    datos = clientes_controllers.cli_registro()
    return datos

@clientes_bp.route('/<string:uuid>', methods=['DELETE'])
@token_requerido
def eliminar(uuid):
    datos = clientes_controllers.cli_eliminacion(uuid)
    return datos

@clientes_bp.route('/<string:uuid>', methods=['PUT'])
@token_requerido
def actualizar(uuid):
    datos = clientes_controllers.cli_actualizacion(uuid)
    return datos