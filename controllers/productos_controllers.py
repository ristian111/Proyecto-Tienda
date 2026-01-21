from flask import jsonify, request
from services import productos_services, categorias_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def prod_listado():
    # Devuelve en formato json el listado de pedidos junto al codigo http 
    datos = productos_services.listar_productos()
    return jsonify(datos), 200

@manejo_errores
def prod_registro():
    # Valida que no existan campos vacios
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["nombre", "precio_venta", "precio_compra", "unidad_medida", "ref_categoria"])

    if validar_requeridos:
        return validar_requeridos

    # Guarda los valores de la petición en variables
    nombre          = data['nombre']
    precio_venta    = data['precio_venta']
    precio_compra   = data['precio_compra']
    unidad_medida   = data['unidad_medida']
    categoria_uuid  = data['ref_categoria']

    # Valida los campos numericos para verificar que cumplen esta regla
    try:
        precio_venta  = float(precio_venta)
        precio_compra = float(precio_compra)
    except ValueError:
        return jsonify({"mensaje": "Los campos precio_venta y precio_compra deben ser números"}), 400
    
    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    validar_datos = controllers.limpieza_datos(
        {"nombre": nombre, "precio_venta": precio_venta, "precio_compra": precio_compra, 
         "unidad_medida": unidad_medida, "ref_categoria": categoria_uuid})

    if validar_datos:
        return validar_datos
    
    # Valida a través de operadores de comparación para asegurar los datos
    if precio_venta <= 0:
        return jsonify({"mensaje": "precio_venta debe ser mayor a 0"}), 400

    if precio_compra < 0:
        return jsonify({"mensaje": "precio_compra no puede ser negativo"}), 400

    if precio_compra > precio_venta:
        return jsonify({"mensaje": "precio_compra no puede ser mayor que precio_venta"}), 400

    # Revisa si la referencia de la categoria existe a través del uuid
    categoria = categorias_services.obtener_categoria_por_uuid(categoria_uuid.strip())
    if not categoria:
        return jsonify({"mensaje": "La categoría no existe"}), 404

    # Donde se guarda en una variable para acceder a la id del producto
    categoria_id = categoria['id']

    commit = productos_services.registrar_producto(nombre.strip(), precio_venta, precio_compra, unidad_medida.strip(), categoria_id)
    if commit:
        return jsonify({"mensaje": "Producto registrado exitosamente"}), 201
    return jsonify({"mensaje": "Error al registrar producto"}), 500

@manejo_errores
def prod_eliminacion(uuid):
    # Valida la existencia del producto a través del uuid 
    producto = productos_services.obtener_producto_por_uuid(uuid)

    if producto:
        commit = productos_services.eliminar_producto(uuid)
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
    
    try:
        precio_venta  = float(precio_venta)
        precio_compra = float(precio_compra)
    except ValueError:
        return jsonify({"mensaje": "Los campos precio_venta y precio_compra deben ser números"}), 400

    if precio_venta <= 0:
        return jsonify({"mensaje": "precio_venta debe ser mayor a 0"}), 400

    if precio_compra < 0:
        return jsonify({"mensaje": "precio_compra no puede ser negativo"}), 400

    if precio_compra > precio_venta:
        return jsonify({"mensaje": "precio_compra no puede ser mayor que precio_venta"}), 400

    validar_datos = controllers.limpieza_datos(
        {"nombre": nombre, "precio_venta": precio_venta, "precio_compra": precio_compra, 
         "unidad_medida": unidad_medida, "ref_categoria": categoria_uuid})

    if validar_datos:
        return validar_datos

    categoria = categorias_services.obtener_categoria_por_uuid(categoria_uuid.strip())
    if not categoria:
        return jsonify({"mensaje": "La categoría no existe"}), 404
    
    categoria_id = categoria['id']

    commit = productos_services.actualizar_producto(uuid.strip(), nombre.strip(), precio_venta, precio_compra, unidad_medida.strip(), categoria_id)
    if commit:
        return jsonify({"mensaje": "Producto actualizado exitosamente"}), 201
    return jsonify({"mensaje": "Error al actualizar producto"}), 500