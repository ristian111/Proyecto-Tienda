from flask import Blueprint
from controllers import clientes_controllers

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
def listar():
    datos = clientes_controllers.cli_listado()
    return datos

@clientes_bp.route('/', methods=['POST'])
def registrar():
    datos = clientes_controllers.cli_registro()
    return datos

@clientes_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = clientes_controllers.cli_eliminacion(uuid)
    return datos

@clientes_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = clientes_controllers.cli_actualizacion(uuid)
    return datos