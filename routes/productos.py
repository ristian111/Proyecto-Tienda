from flask import Blueprint
from controllers import productos_controllers
productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
def listar():
    datos = productos_controllers.prod_listado()
    return datos

@productos_bp.route('/', methods=['POST'])
def registrar():
    datos = productos_controllers.prod_registro()
    return datos

@productos_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = productos_controllers.prod_eliminacion(uuid)
    return datos

@productos_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = productos_controllers.prod_actualizacion(uuid)
    return datos