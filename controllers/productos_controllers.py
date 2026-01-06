from flask import jsonify, request
from services.productos_services import listar_productos, registrar_producto, actualizar_producto, eliminar_producto, obtener_producto_por_uuid
from services.categorias_services import obtener_categoria_por_uuid

def prod_listado():
    # Devuelve en formato json el listado de pedidos junto al codigo http 
    datos = listar_productos()
    return jsonify(datos), 200

def prod_registro():
    # Valida que no existan campos vacios
    data = request.get_json()

    requeridos = ["nombre", "precio_venta", "precio_compra", "unidad_medida", "ref_categoria"]
    faltantes = [x for x in requeridos if x not in data]
    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400

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
    if not isinstance(nombre, str) or len(nombre.strip()) == 0:
        return jsonify({"mensaje": "El nombre no puede estar vacío"}), 400
    
    if not isinstance(unidad_medida, str) or len(unidad_medida.strip()) == 0:
        return jsonify({"mensaje": "unidad_medida debe ser una cadena de texto o no puede estar vacia"}), 400
    
    if not isinstance(categoria_uuid, str) or len(categoria_uuid.strip()) == 0:
        return jsonify({"mensaje": "ref_categoria debe ser una cadena de texto o no puede estar vacia"}), 400

    # Valida a través de operadores de comparación para asegurar los datos
    if precio_venta <= 0:
        return jsonify({"mensaje": "precio_venta debe ser mayor a 0"}), 400

    if precio_compra < 0:
        return jsonify({"mensaje": "precio_compra no puede ser negativo"}), 400

    if precio_compra > precio_venta:
        return jsonify({"mensaje": "precio_compra no puede ser mayor que precio_venta"}), 400

    # Revisa si la referencia de la categoria existe a través del uuid
    categoria = obtener_categoria_por_uuid(categoria_uuid)
    if not categoria:
        return jsonify({"mensaje": "La categoría no existe"}), 404

    # Donde se guarda en una variable para acceder a la id del producto
    categoria_id = categoria['id']

    commit = registrar_producto(nombre, precio_venta, precio_compra, unidad_medida, categoria_id)
    if commit:
        return jsonify({"mensaje": "Producto registrado exitosamente"}), 201
    return jsonify({"mensaje": "Error al registrar producto"}), 500

def prod_eliminacion(uuid):
    # Valida la existencia del producto a través del uuid 
    producto = obtener_producto_por_uuid(uuid)

    if producto:
        commit = eliminar_producto(uuid)
        if commit:
            return jsonify({"mensaje": "Producto eliminado exitosamente"}), 200
        
        return jsonify({"mensaje": "Error al eliminar producto"}), 500
    return jsonify({"mensaje": "El producto no existe"}), 404

# Se valida de la misma manera que al registrar
def prod_actualizacion(uuid):
    data = request.get_json()

    requeridos = ["nombre", "precio_venta", "precio_compra", "unidad_medida", "ref_categoria"]
    faltantes = [x for x in requeridos if x not in data]
    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
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
    
    if not isinstance(nombre, str) or len(nombre.strip()) == 0:
        return jsonify({"mensaje": "El nombre no puede estar vacío"}), 400

    if precio_venta <= 0:
        return jsonify({"mensaje": "precio_venta debe ser mayor a 0"}), 400

    if precio_compra < 0:
        return jsonify({"mensaje": "precio_compra no puede ser negativo"}), 400

    if precio_compra > precio_venta:
        return jsonify({"mensaje": "precio_compra no puede ser mayor que precio_venta"}), 400

    if not isinstance(unidad_medida, str) or len(unidad_medida.strip()) == 0:
        return jsonify({"mensaje": "unidad_medida debe ser una cadena de texto o no puede estar vacia"}), 400
    
    if not isinstance(categoria_uuid, str) or len(categoria_uuid.strip()) == 0:
        return jsonify({"mensaje": "ref_categoria debe ser una cadena de texto o no puede estar vacia"}), 400

    categoria = obtener_categoria_por_uuid(categoria_uuid)
    if not categoria:
        return jsonify({"mensaje": "La categoría no existe"}), 404
    
    categoria_id = categoria['id']

    commit = actualizar_producto(uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_id)
    if commit:
        return jsonify({"mensaje": "Producto actualizado exitosamente"}), 200
    return jsonify({"mensaje": "Error al actualizar producto"}), 500