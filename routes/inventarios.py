from flask import Blueprint
from security import token_requerido
from controllers import inventarios_controllers

inventarios_bp = Blueprint('inventarios', __name__)

@inventarios_bp.route('/', methods=['GET'])
def listar():
    datos = inventarios_controllers.inv_listado()
    return datos

@inventarios_bp.route('/', methods=['POST'])
@token_requerido
def registrar():
    datos = inventarios_controllers.inv_registro()
    return datos

@inventarios_bp.route('/<string:uuid>', methods=['DELETE'])
@token_requerido
def eliminar(uuid):
    datos = inventarios_controllers.inv_eliminacion(uuid)
    return datos

@inventarios_bp.route('/<string:uuid>', methods=['PUT'])
@token_requerido
def actualizar(uuid):
    datos = inventarios_controllers.inv_actualizacion(uuid)
    return datos

@inventarios_bp.route('/stock-bajo', methods=['GET'])
def listar_productos_con_stock_bajo():
    datos = inventarios_controllers.inv_productos_stock_bajo()
    return datos

@inventarios_bp.route('/<string:producto>/productos', methods=['GET'])
def listar_stock_producto(producto):
    datos = inventarios_controllers.inv_stock_producto(producto)
    return datos

@inventarios_bp.route('/movimiento-inventario', methods=['GET'])
def listar_movimiento_inventario():
    datos = inventarios_controllers.inv_listado_movimiento_inventario()
    return datos