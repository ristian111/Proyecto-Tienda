from flask import jsonify, request
from . import validar_campos
from services import (listar_categorias, registrar_categoria, actualizar_categoria, eliminar_categoria, 
                      obtener_categoria_por_uuid)

def cat_listado():
    # Devuelve en formato json el listado de categorias junto al codigo http 
    datos = listar_categorias()
    return jsonify(datos), 200

def cat_registro():
    # Valida que no existan campos vacios 
    data = request.get_json()

    validar_requeridos = validar_campos(data, ["nombre", descripcion])

    if validar_requeridos:
        return validar_requeridos
    
    # Guarda los valores de la petición en variables
    nombre      = data['nombre'].strip()
    descripcion = data['descripcion'].strip()

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    if not isinstance(nombre, str) or nombre == "":
        return jsonify({"mensaje": "El nombre debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(descripcion, str) or descripcion == "":
        return jsonify({"mensaje": "La descripcion debe ser una cadena de texto o no puede estar vacia"}), 400

    commit = registrar_categoria(nombre, descripcion)
    if commit:
        return jsonify({"mensaje": "Categoria registrada exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar categoria"}), 500

def cat_eliminacion(uuid):
    # Valida la existencia de la categoria a través del uuid 
    categoria = obtener_categoria_por_uuid(uuid)
    if categoria:
        commit = eliminar_categoria(uuid)
        if commit:
            return jsonify({"mensaje": "Categoria eliminada exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar categoria"}), 500
    return jsonify({"mensaje": "La categoria no existe"}), 404

# Se valida de la misma manera que al registrar
def cat_actualizacion(uuid):
    data = request.get_json()

    requeridos = ["nombre", "descripcion"]
    faltantes = [x for x in requeridos if x not in data]
    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
    nombre      = data['nombre'].strip()
    descripcion = data['descripcion'].strip()

    if not isinstance(nombre, str) or nombre == "":
        return jsonify({"mensaje": "El nombre debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(descripcion, str) or descripcion == "":
        return jsonify({"mensaje": "El descripcion debe ser una cadena de texto o no puede estar vacio"}), 400
    
    commit = actualizar_categoria(uuid, nombre, descripcion)
    if commit:
        return jsonify({"mensaje": "Categoria actualizada exitosamente"}), 201
    return jsonify({"mensaje": "Error al actualizar categoria"}), 500