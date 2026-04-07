from flask import jsonify, request
from services import estadisticas_service
from decoradores import manejo_errores

@manejo_errores
def resumen_hoy():
    uuid_usuario = request.usuario['uuid']
    datos = estadisticas_service.resumen_hoy(uuid_usuario)
    return jsonify(datos), 200

@manejo_errores
def top_productos():
    uuid_usuario = request.usuario['uuid']
    filtro = request.args.get('filtro', 'mensual')
    datos = estadisticas_service.top_productos(uuid_usuario, filtro)
    return jsonify(datos), 200

@manejo_errores
def ingresos_ganancias():
    uuid_usuario = request.usuario['uuid']
    dias = int(request.args.get('dias', 7))
    datos = estadisticas_service.ingresos_ganancias(uuid_usuario, dias)
    return jsonify(datos), 200

@manejo_errores
def horas_pico():
    uuid_usuario = request.usuario['uuid']
    datos = estadisticas_service.horas_pico(uuid_usuario)
    return jsonify(datos), 200

@manejo_errores
def productos_estancados():
    uuid_usuario = request.usuario['uuid']
    datos = estadisticas_service.productos_estancados(uuid_usuario)
    return jsonify(datos), 200

@manejo_errores
def porcentaje_categorias():
    uuid_usuario = request.usuario['uuid']
    datos = estadisticas_service.porcentaje_categorias(uuid_usuario)
    return jsonify(datos), 200
