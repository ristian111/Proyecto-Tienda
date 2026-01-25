from flask import jsonify, request
import controllers
from services import categorias_services
from decoradores import manejo_errores

@manejo_errores
def cat_listado():
    # Devuelve en formato json el listado de categorias junto al codigo http 
    datos = categorias_services.listar_categorias()
    return jsonify(datos), 200

@manejo_errores
def cat_registro():

    data = request.get_json()

    # Valida que no existan campos vacios
    validar_requeridos = controllers.validar_campos(data, ["nombre", "descripcion"])

    if validar_requeridos:
        return validar_requeridos
    
    # Guarda los valores de la petición en variables
    nombre      = data['nombre']
    descripcion = data['descripcion']

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    validar_datos = controllers.limpieza_datos({"nombre": nombre, "descripcion": descripcion})

    if validar_datos:
        return validar_datos
    
    try:
        commit = categorias_services.registrar_categoria(nombre.strip(), descripcion.strip())
        return jsonify({"mensaje": "Categoria registrada exitosamente",
                        "Categoría": commit}), 201
    except RuntimeError as e:
        return jsonify({"mensaje": str(e)}), 500

@manejo_errores
def cat_eliminacion(uuid):
    # Valida la existencia de la categoria a través del uuid 
    categoria = categorias_services.obtener_categoria_por_uuid(uuid)
    if categoria:
        commit = categorias_services.eliminar_categoria(uuid)
        if commit:
            return jsonify({"mensaje": "Categoria eliminada exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar categoria"}), 500
    return jsonify({"mensaje": "La categoría no existe"}), 404

@manejo_errores
# Se valida de la misma manera que al registrar
def cat_actualizacion(uuid):
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["nombre", "descripcion"])

    if validar_requeridos:
        return validar_requeridos

    nombre      = data['nombre'].strip()
    descripcion = data['descripcion'].strip()
 
    validar_datos = controllers.limpieza_datos({"nombre": nombre, "descripcion": descripcion})

    if validar_datos:
        return validar_datos
    
    categoria = categorias_services.obtener_categoria_por_uuid(uuid)
    if categoria:
        try:
            commit = categorias_services.actualizar_categoria(uuid, nombre, descripcion)
            return jsonify({"mensaje": "Categoria actualizada exitosamente",
                            "Categoría": commit}), 200
        except Exception:
            return jsonify({"mensaje: Error al actualizar categoría"}), 500
    return jsonify({"mensaje": "La categoría no existe"}), 404