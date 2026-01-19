from flask import Blueprint
from middlewares import require_api_key
from controllers import cat_listado, cat_registro, cat_actualizacion, cat_eliminacion
categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
@require_api_key
def listar():
    datos = cat_listado()
    return datos

@categorias_bp.route('/', methods=['POST'])
def registrar():
    datos = cat_registro()
    return datos

@categorias_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = cat_eliminacion(uuid)
    return datos

@categorias_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = cat_actualizacion(uuid)
    return datos
