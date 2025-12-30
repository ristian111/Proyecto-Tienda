from flask import blueprints, jsonify
from controllers.facturas_controllers import fac_listado, fac_registro, fac_actualizacion, fac_eliminacion
facturas_bp = blueprints.Blueprint('facturas', __name__)

@facturas_bp.route('/', methods=['GET'])
def listar():
    datos = fac_listado()
    return datos

@facturas_bp.route('/', methods=['POST'])
def registrar():
    datos = fac_registro()
    return datos

@facturas_bp.route('/<string:uuid>', methods=['DELETE'])
def eliminar(uuid):
    datos = fac_eliminacion(uuid)
    return datos

@facturas_bp.route('/<string:uuid>', methods=['PUT'])
def actualizar(uuid):    
    datos = fac_actualizacion(uuid)
    return datos