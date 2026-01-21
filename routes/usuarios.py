from flask import Blueprint
from controllers import usuarios_controllers
from security import token_requerido, rol_requerido
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
@token_requerido
@rol_requerido("Administrador")
def listar():
    datos = usuarios_controllers.usu_listado()
    return datos

@usuarios_bp.route('/', methods=['POST'])
def registrar():
    datos = usuarios_controllers.usu_registro()
    return datos

@usuarios_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = usuarios_controllers.usu_eliminacion(uuid)
    return datos

@usuarios_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = usuarios_controllers.usu_actualizacion(uuid)
    return datos

@usuarios_bp.route('<string:user>/pedidos', methods=['GET'])
def buscar_pedidos_por_usuario(user):
    datos = usuarios_controllers.usu_pedidos_usuario(user)
    return datos