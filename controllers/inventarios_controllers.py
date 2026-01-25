from flask import jsonify, request
from services import inventarios_services, productos_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def inv_listado():
    # Devuelve en formato json el listado de inventarios junto al codigo http 
    datos = inventarios_services.listar_inventarios()
    return jsonify(datos), 200

@manejo_errores
def inv_listado_movimiento_inventario():
    datos = inventarios_services.listar_movimiento_inventario()
    return jsonify(datos), 200

@manejo_errores
def inv_registro():
    # Valida que no existan campos vacios 
    data = request.get_json()

    validar_datos = controllers.validar_campos(data, ["ref_producto", "cantidad_actual", "cantidad_reservada", "punto_reorden"])
    
    if validar_datos:
        return validar_datos
    
    # Guarda los valores de la petición en variables
    producto_uuid      = data['ref_producto']
    cantidad_actual    = data['cantidad_actual']
    cantidad_reservada = data['cantidad_reservada']
    punto_reorden      = data['punto_reorden']

    # Valida los campos numericos para verificar que cumplen esta regla
    try:
        cantidad_actual    = int(cantidad_actual)
        cantidad_reservada = int(cantidad_reservada)
        punto_reorden      = int(punto_reorden)
    except ValueError:
        return jsonify({"mensaje": "Los campos cantidad_actual, cantidad_reservada y punto_reorden deben ser números enteros"}), 400
    
    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    validar_datos = controllers.limpieza_datos({"ref_producto": producto_uuid})

    if validar_datos:
        return validar_datos

    # Revisa si la referencia del producto existe a través del uuid
    producto = productos_services.obtener_producto_por_uuid(producto_uuid.strip())
    if not producto:
        return jsonify({"mensaje": "El producto no existe"}), 404

    # Donde se guarda en una variable para acceder a la id del producto
    producto_id = producto['id']

    try:
        commit = inventarios_services.registrar_inventario(producto_id, cantidad_actual, cantidad_reservada, punto_reorden)
        return jsonify({"mensaje": "Inventario registrado exitosamente",
                        "Inventario": commit}), 201
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"mensaje": str(e)}), 500

@manejo_errores
def inv_eliminacion(uuid):
    # Valida la existencia del inventario a través del uuid 
    inventario = inventarios_services.obtener_inventario_por_uuid(uuid)

    if inventario:
        commit = inventarios_services.eliminar_inventario(uuid)
        if commit:
            return jsonify({"mensaje": "Inventario eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar inventario"}), 500
    return jsonify({"mensaje": "El inventario no existe"}), 404

@manejo_errores
# Se valida de la misma manera que al registrar
def inv_actualizacion(uuid):
    data = request.get_json()

    validar_datos = controllers.validar_campos(data, ["ref_producto", "cantidad_actual", "cantidad_reservada", "punto_reorden"])
    
    if validar_datos:
        return validar_datos
    
    producto_uuid      = data['ref_producto']
    cantidad_actual    = data['cantidad_actual']
    cantidad_reservada = data['cantidad_reservada']
    punto_reorden      = data['punto_reorden']
    
    try:
        cantidad_actual    = int(cantidad_actual)
        cantidad_reservada = int(cantidad_reservada)
        punto_reorden      = int(punto_reorden)
    except ValueError:
        return jsonify({"mensaje": "Los campos cantidad_actual, cantidad_reservada y punto_reorden deben ser números enteros"}), 400
    
    validar_datos = controllers.limpieza_datos({"ref_producto": producto_uuid})

    if validar_datos:
        return validar_datos
    
    producto = productos_services.obtener_producto_por_uuid(producto_uuid.strip())
    if not producto:
        return jsonify({"mensaje": "El producto no existe"}), 404

    producto_id = producto['id']
    inventario = inventarios_services.obtener_inventario_por_uuid(uuid)
    if inventario:
        try:
            commit = inventarios_services.actualizar_inventario(uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden, producto_uuid.strip())
            return jsonify({"mensaje": "Inventario actualizado exitosamente",
                            "Inventario": commit}), 200
        except ValueError as e:
            return jsonify({"mensaje": str(e)}), 400
        except Exception:
            return jsonify({"mensaje": "Error al actualizar inventario"}), 500
    return jsonify({"mensaje": "El inventario no existe"}), 404

@manejo_errores
def inv_productos_stock_bajo():

    limite = request.args.get("limit", default=1, type=int)

    commit = inventarios_services.listar_productos_stock_bajo(limite)

    if commit:
        return jsonify({"mensaje": "Producto encontrado exitosamente",
                        "Stock producto": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar producto"}), 500

@manejo_errores
def inv_stock_producto(producto):

    commit = inventarios_services.listar_stock_producto(producto)
        
    if commit:
        return jsonify({"mensaje": "Producto encontrado exitosamente",
                        "Stock producto": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar producto"}), 500