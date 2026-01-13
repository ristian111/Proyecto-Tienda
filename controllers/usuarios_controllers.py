from flask import jsonify, request, current_app
from services.usuarios_services import listar_usuarios, registrar_usuario, actualizar_usuario, eliminar_usuario, obtener_usuario_por_uuid, pedidos_de_un_usuario

def usu_listado():
    # Devuelve en formato json el listado de pedidos junto al codigo http 
    datos = listar_usuarios()
    return jsonify(datos), 200

def usu_registro():
    # Valida que no existan campos vacios
    data = request.get_json()

    requeridos = ["nombre", "username", "password_hash", "rol"]
    faltantes = [x for x in requeridos if x not in data]
    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400

    # Guarda los valores de la petición en variables
    nombre        = data['nombre']
    username      = data['username']
    password_hash = data['password_hash']
    rol           = data['rol']

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    if not isinstance(nombre, str) or nombre.strip() == "":
        return jsonify({"mensaje": "El nombre debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(username, str) or username.strip() == "":
        return jsonify({"mensaje": "El username debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(rol, str) or rol.strip() == "":
        return jsonify({"mensaje": "El rol debe ser una cadena de texto o no puede estar vacio"}), 400

    # Valida a través de operadores de comparación para asegurar los datos
    if len(username.strip()) < 10:
        return jsonify({"mensaje": "El username debe tener al menos 10 caracteres"}), 400
    
    if len(password_hash.strip()) < 10:
        return jsonify({"mensaje": "La contraseña debe tener al menos 10 caracteres"}), 400
    
    # Genera un hash de la contraseña donde se envia a la base de datos
    pass_encriptado = current_app.bcrypt.generate_password_hash(password_hash)
    
    commit = registrar_usuario(nombre, username, pass_encriptado, rol) 
    if commit:
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201
    
    return jsonify({"mensaje": "Error al registrar usuario"}), 500

def usu_eliminacion(uuid):
    # Valida la existencia del usuario a través del uuid 
    usuario = obtener_usuario_por_uuid(uuid)

    if usuario:
        commit = eliminar_usuario(uuid)
        if commit:
            return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar usuario"}), 500
    return jsonify({"mensaje": "El usuario no existe"}), 404

# Se valida de la misma manera que al registrar
def usu_actualizacion(uuid):
    data = request.get_json()

    requeridos = ["nombre", "username", "password_hash", "rol"]
    faltantes = [x for x in requeridos if x not in data]
    if faltantes:
        return jsonify({"mensaje":f"faltan los campos {faltantes}"}), 400
    
    nombre        = data['nombre']
    username      = data['username']
    password_hash = data['password_hash']
    rol           = data['rol']

    if not isinstance(nombre, str) or nombre.strip() == "":
        return jsonify({"mensaje": "El nombre debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if not isinstance(username, str) or username.strip() == "":
        return jsonify({"mensaje": "El username debe ser una cadena de texto o no puede estar vacio"}), 400

    if len(username.strip()) < 10:
        return jsonify({"mensaje": "El nombre debe tener al menos 10 caracteres"}), 400
    
    if not isinstance(rol, str) or rol.strip() == "":
        return jsonify({"mensaje": "El rol debe ser una cadena de texto o no puede estar vacio"}), 400
    
    if len(password_hash.strip()) < 10:
        return jsonify({"mensaje": "La contraseña debe tener al menos 10 caracteres"}), 400
    
    pass_encriptado = current_app.bcrypt.generate_password_hash(password_hash)

    commit = actualizar_usuario(uuid, nombre, username, pass_encriptado, rol)
    if commit:
        return jsonify({"mensaje": "Usuario actualizado exitosamente"}), 200
    return jsonify({"mensaje": "Error al actualizar usuario"}), 500

def usu_pedidos_usuario(user):

    commit = pedidos_de_un_usuario(user)
    if commit:
        return jsonify({"mensaje": "Usuario encontrado exitosamente",
                        "pedidos_por_usuario": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar usuario"}), 500