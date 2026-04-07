from flask import jsonify, request
from services import productos_services, categorias_services, inventarios_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def prod_listado():
    # Devuelve en formato json el listado de pedidos junto al codigo http 
    uuid_usuario = request.usuario['uuid']
    datos = productos_services.listar_productos(uuid_usuario)
    return jsonify(datos), 200

@manejo_errores
def prod_registro():
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["nombre", "precio_venta", "precio_compra", "unidad_medida", "ref_categoria", "cantidad_actual"])

    if validar_requeridos:
        return validar_requeridos

    # Guarda los valores de la petición en variables
    nombre          = data['nombre']
    precio_venta    = data['precio_venta']
    precio_compra   = data['precio_compra']
    unidad_medida   = data['unidad_medida']
    categoria_uuid  = data['ref_categoria']
    cantidad_actual = data['cantidad_actual']

    # Valida los campos numericos para verificar que cumplen esta regla
    validar_numeros = controllers.limpieza_numeros({"precio_venta": precio_venta, "precio_compra": precio_compra, "cantidad_actual": cantidad_actual})
    
    if validar_numeros:
        return validar_numeros
    
    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    validar_datos = controllers.limpieza_datos(
        {"nombre": nombre, "unidad_medida": unidad_medida, "ref_categoria": categoria_uuid})

    if validar_datos:
        return validar_datos

    uuid_usuario = request.usuario['uuid']
    # Revisa si la referencia de la categoria existe a través del uuid
    categoria = categorias_services.obtener_categoria_por_uuid(categoria_uuid.strip(), uuid_usuario)
    if not categoria:
        return jsonify({"mensaje": "La categoría no existe"}), 404

    # Donde se guarda en una variable para acceder a la id del producto
    categoria_id = categoria['id']

    commit = productos_services.registrar_producto(nombre.strip(), precio_venta, precio_compra, unidad_medida.strip(), categoria_id, categoria_uuid.strip(), uuid_usuario)
    
    producto_creado = productos_services.obtener_producto_por_uuid(commit['ref'], uuid_usuario)
    if producto_creado:
        inventarios_services.registrar_inventario(producto_creado['id'], cantidad_actual, 0, 0)
        
    return jsonify({"mensaje": "Producto registrado exitosamente",
                    "Producto": commit}), 201
    
@manejo_errores
def prod_eliminacion(uuid):
    uuid_usuario = request.usuario['uuid']
    # Valida la existencia del producto a través del uuid 
    producto = productos_services.obtener_producto_por_uuid(uuid, uuid_usuario)

    if producto:
        commit = productos_services.eliminar_producto(uuid, uuid_usuario)
        if commit:
            return jsonify({"mensaje": "Producto eliminado exitosamente"}), 200
        
        return jsonify({"mensaje": "Error al eliminar producto"}), 500
    return jsonify({"mensaje": "El producto no existe"}), 404

@manejo_errores
# Se valida de la misma manera que al registrar
def prod_actualizacion(uuid):
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["nombre", "precio_venta", "precio_compra", "unidad_medida", "ref_categoria"])

    if validar_requeridos:
        return validar_requeridos
    
    nombre          = data['nombre']
    precio_venta    = data['precio_venta']
    precio_compra   = data['precio_compra']
    unidad_medida   = data['unidad_medida']
    categoria_uuid  = data['ref_categoria']
    
    validar_numeros = controllers.limpieza_numeros({"precio_venta": precio_venta, "precio_compra": precio_compra})
    
    if validar_numeros:
        return validar_numeros

    validar_datos = controllers.limpieza_datos(
        {"nombre": nombre, "unidad_medida": unidad_medida, "ref_categoria": categoria_uuid})

    if validar_datos:
        return validar_datos

    uuid_usuario = request.usuario['uuid']
    categoria = categorias_services.obtener_categoria_por_uuid(categoria_uuid.strip(), uuid_usuario)
    if not categoria:
        return jsonify({"mensaje": "La categoría no existe"}), 404
    
    categoria_id = categoria['id']
    
    producto = productos_services.obtener_producto_por_uuid(uuid, uuid_usuario)
    if producto:
            
        commit = productos_services.actualizar_producto(uuid.strip(), nombre.strip(), precio_venta, precio_compra, unidad_medida.strip(), categoria_id, categoria_uuid.strip(), uuid_usuario)
        return jsonify({"mensaje": "Producto actualizado exitosamente",
                        "Producto": commit}), 200
        
    return jsonify({"mensaje": "El producto no existe"}), 404