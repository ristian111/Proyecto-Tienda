from flask import Blueprint
from controllers.usuarios_controllers import usu_listado, usu_actualizacion, usu_eliminacion, usu_registro
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
def listar():
    datos = usu_listado()
    return datos

@usuarios_bp.route('/', methods=['POST'])
def registrar():
    datos = usu_registro()
    return datos

@usuarios_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = usu_eliminacion(uuid)
    return datos

@usuarios_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = usu_actualizacion(uuid)
    return datos