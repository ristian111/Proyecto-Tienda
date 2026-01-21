from flask import Blueprint
from security import api_key_requerido
from controllers import categorias_controller
categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
@api_key_requerido
def listar():
    datos = categorias_controller.cat_listado()
    return datos

@categorias_bp.route('/', methods=['POST'])
def registrar():
    datos = categorias_controller.cat_registro()
    return datos

@categorias_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = categorias_controller.cat_eliminacion(uuid)
    return datos

@categorias_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = categorias_controller.cat_actualizacion(uuid)
    return datos
