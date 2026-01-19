from flask import Blueprint
from middlewares import token_requerido
from controllers import (inv_listado, inv_actualizacion, inv_eliminacion, inv_registro, 
                         inv_productos_stock_bajo, inv_stock_producto, inv_listado_movimiento_inventario)

inventarios_bp = Blueprint('inventarios', __name__)

@inventarios_bp.route('/', methods=['GET'])
def listar():
    datos = inv_listado()
    return datos

@inventarios_bp.route('/', methods=['POST'])
@token_requerido
def registrar():
    datos = inv_registro()
    return datos

@inventarios_bp.route('/<string:uuid>', methods=['DELETE'])
@token_requerido
def eliminar(uuid):
    datos = inv_eliminacion(uuid)
    return datos

@inventarios_bp.route('/<string:uuid>', methods=['PUT'])
@token_requerido
def actualizar(uuid):
    datos = inv_actualizacion(uuid)
    return datos

@inventarios_bp.route('/stock-bajo', methods=['GET'])
def listar_productos_con_stock_bajo():
    datos = inv_productos_stock_bajo()
    return datos

@inventarios_bp.route('/<string:producto>/productos', methods=['GET'])
def listar_stock_producto(producto):
    datos = inv_stock_producto(producto)
    return datos

@inventarios_bp.route('/movimiento-inventario', methods=['GET'])
def listar_movimiento_inventario():
    datos = inv_listado_movimiento_inventario()
    return datos