from flask import Blueprint
from security import token_requerido
from controllers import categorias_controller
categorias_bp = Blueprint('categorias_v1', __name__)

@categorias_bp.route('/', methods=['GET'])
@token_requerido
def listar():
    datos = categorias_controller.cat_listado()
    return datos

@categorias_bp.route('/', methods=['POST'])
@token_requerido
def registrar():
    datos = categorias_controller.cat_registro()
    return datos

@categorias_bp.route('/<string:uuid>', methods=['DELETE'])
@token_requerido
def eliminar(uuid):
    datos = categorias_controller.cat_eliminacion(uuid)
    return datos

@categorias_bp.route('/<string:uuid>', methods=['PUT'])
@token_requerido
def actualizar(uuid):
    datos = categorias_controller.cat_actualizacion(uuid)
    return datos
