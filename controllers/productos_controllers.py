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
        {"nombre": nombre, "unidad_medida": unidad_medida, "ref_categoria": categoria_uuid})

    if validar_datos:
        return validar_datos

    # Revisa si la referencia de la categoria existe a través del uuid
    categoria = categorias_services.obtener_categoria_por_uuid(categoria_uuid.strip())
    if not categoria:
        return jsonify({"mensaje": "La categoría no existe"}), 404

    # Donde se guarda en una variable para acceder a la id del producto
    categoria_id = categoria['id']

    try:
        commit = productos_services.registrar_producto(nombre.strip(), precio_venta, precio_compra, unidad_medida.strip(), categoria_id, categoria_uuid.strip())
        return jsonify({"mensaje": "Producto registrado exitosamente",
                        "Producto": commit}), 201
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"mensaje": str(e)}), 500

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

    validar_datos = controllers.limpieza_datos(
        {"nombre": nombre, "unidad_medida": unidad_medida, "ref_categoria": categoria_uuid})

    if validar_datos:
        return validar_datos

    categoria = categorias_services.obtener_categoria_por_uuid(categoria_uuid.strip())
    if not categoria:
        return jsonify({"mensaje": "La categoría no existe"}), 404
    
    categoria_id = categoria['id']
    
    producto = productos_services.obtener_producto_por_uuid(uuid)
    if producto:
        try:
            commit = productos_services.actualizar_producto(uuid.strip(), nombre.strip(), precio_venta, precio_compra, unidad_medida.strip(), categoria_id, categoria_uuid.strip())
            return jsonify({"mensaje": "Producto actualizado exitosamente",
                            "Producto": commit}), 200
        except ValueError as e:
            return jsonify({"mensaje": str(e)}), 400
        except Exception:
            return jsonify({"mensaje": "Error al actualizar producto"}), 500
    return jsonify({"mensaje": "El producto no existe"}), 404