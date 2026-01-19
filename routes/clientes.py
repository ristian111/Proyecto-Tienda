from flask import Blueprint
from controllers import cli_listado, cli_actualizacion, cli_registro, cli_eliminacion

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
def listar():
    datos = cli_listado()
    return datos

@clientes_bp.route('/', methods=['POST'])
def registrar():
    datos = cli_registro()
    return datos

@clientes_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = cli_eliminacion(uuid)
    return datos

@clientes_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = cli_actualizacion(uuid)
    return datos