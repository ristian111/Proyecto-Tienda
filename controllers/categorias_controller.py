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
    
    commit = categorias_services.registrar_categoria(nombre.strip(), descripcion.strip())
    if commit:
        return jsonify({"mensaje": "Categoria registrada exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar categoria"}), 500

@manejo_errores
def cat_eliminacion(uuid):
    # Valida la existencia de la categoria a través del uuid 
    categoria = categorias_services.obtener_categoria_por_uuid(uuid)
    if categoria:
        commit = categorias_services.eliminar_categoria(uuid)
        if commit:
            return jsonify({"mensaje": "Categoria eliminada exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar categoria"}), 500
    return jsonify({"mensaje": "La categoria no existe"}), 404

@manejo_errores
# Se valida de la misma manera que al registrar
def cat_actualizacion(uuid):
    data = request.get_json()

    # Valida que no existan campos vacios
    validar_requeridos = controllers.validar_campos(data, ["nombre", "descripcion"])

    if validar_requeridos:
        return validar_requeridos
    
    # Guarda los valores de la petición en variables
    nombre      = data['nombre'].strip()
    descripcion = data['descripcion'].strip()

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    validar_datos = controllers.limpieza_datos([nombre, descripcion])

    if validar_datos:
        return validar_datos
    
    commit = categorias_services.actualizar_categoria(uuid, nombre, descripcion)
    if commit:
        return jsonify({"mensaje": "Categoria actualizada exitosamente"}), 200
    return jsonify({"mensaje": "Error al actualizar categoria"}), 500