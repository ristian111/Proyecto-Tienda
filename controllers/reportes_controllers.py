from flask import jsonify, request
from datetime import datetime, timedelta
from services import reportes_services
from decoradores import manejo_errores

@manejo_errores
def rep_clientes_con_mas_pedidos():
    limit = request.args.get("limit", default=5, type=int)
    uuid_usuario = request.usuario['uuid']
    commit = reportes_services.listar_clientes_con_mas_pedidos(limit, uuid_usuario)
    return jsonify(commit), 200

@manejo_errores
def rep_usuarios_con_mas_pedidos_registrados():
    limit = request.args.get("limit", default=5, type=int)
    uuid_usuario = request.usuario['uuid']
    commit = reportes_services.listar_usuarios_con_mas_registro_pedidos(limit, uuid_usuario)
    if commit:
        return jsonify({"mensaje": "Usuario encontrado exitosamente",
                        "Usuario con mas pedidos registrados": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar usuario"}), 500

@manejo_errores
def rep_productos_mas_vendidos():
    desde  = request.args.get('desde', datetime.utcnow() - timedelta(weeks=4))
    hasta  = request.args.get('hasta', datetime.utcnow())
    limite = request.args.get('limite', default=1, type=int)
    uuid_usuario = request.usuario['uuid']
    commit = reportes_services.listar_productos_mas_vendidos(desde, hasta, limite, uuid_usuario)
    if commit:
        return jsonify({"mensaje": "Producto encontrado exitosamente",
                        "Producto mas vendido": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar producto"}), 500

@manejo_errores
def rep_pedidos_por_fecha():
    desde  = request.args.get('desde', datetime.utcnow() - timedelta(days=1))
    hasta  = request.args.get('hasta', datetime.utcnow())
    estado = request.args.get('estado', default='entregado', type=str)
    uuid_usuario = request.usuario['uuid']

    commit = reportes_services.listar_pedidos_por_fecha(desde, hasta, estado, uuid_usuario)
    if commit:
        return jsonify({"mensaje": "Pedidos encontrados exitosamente",
                        "Pedidos": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar pedidos"}), 500

@manejo_errores
def rep_productos_mas_ganancias():
    desde  = request.args.get('desde', datetime.utcnow() - timedelta(weeks=4))
    hasta  = request.args.get('hasta', datetime.utcnow())
    limite = request.args.get('limite', default=1, type=int)
    uuid_usuario = request.usuario['uuid']

    commit = reportes_services.listar_productos_mas_ganancias(desde, hasta, limite, uuid_usuario)
    if commit:
        return jsonify({"mensaje": "Producto encontrado exitosamente",
                        "Producto con más ganancias": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar producto"}), 500

@manejo_errores
def rep_ingresos_generados():
    desde  = request.args.get('desde', datetime.utcnow() - timedelta(weeks=4))
    hasta  = request.args.get('hasta', datetime.utcnow())
    uuid_usuario = request.usuario['uuid']

    commit = reportes_services.listar_ingresos_por_ventas(desde, hasta, uuid_usuario)
    if commit:
        return jsonify({"mensaje": "Ingresos listados exitosamente",
                        "Ingresos de ventas": commit}), 200
    
    return jsonify({"mensaje": "Error al listar ingresos"}), 500