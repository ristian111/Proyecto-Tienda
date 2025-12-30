from flask import Blueprint
from controllers.inventarios_controllers import inv_listado, inv_actualizacion, inv_eliminacion, inv_registro
inventarios_bp = Blueprint('inventarios', __name__)

@inventarios_bp.route('/', methods=['GET'])
def listar():
    datos = inv_listado()
    return datos

@inventarios_bp.route('/', methods=['POST'])
def registrar():
    datos = inv_registro()
    return datos

@inventarios_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = inv_eliminacion(uuid)
    return datos

@inventarios_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):
    datos = inv_actualizacion(uuid)
    return datos
