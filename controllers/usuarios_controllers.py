from flask import jsonify, request, current_app
from services import usuarios_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def usu_listado():
    # Devuelve en formato json el listado de pedidos junto al codigo http 
    datos = usuarios_services.listar_usuarios()
    return jsonify(datos), 200

@manejo_errores
def usu_registro():
    # Valida que no existan campos vacios
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["nombre", "username", "password_hash", "rol"])

    if validar_requeridos:
        return validar_requeridos

    # Guarda los valores de la petición en variables
    nombre        = data['nombre']
    username      = data['username']
    password_hash = data['password_hash']
    rol           = data['rol']

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    validar_datos = controllers.limpieza_datos(
        {"nombre": nombre, "usuario": username, "contraseña": password_hash, "rol": rol})

    if validar_datos:
        return validar_datos
    
    # Genera un hash de la contraseña donde se envia a la base de datos
    pass_encriptado = current_app.bcrypt.generate_password_hash(password_hash)
    
    try:
        commit = usuarios_services.registrar_usuario(nombre.strip(), username, pass_encriptado, rol.strip().capitalize())  
        return jsonify({"mensaje": "Usuario registrado exitosamente",
                        "Usuario": commit}), 201
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    except Exception:
        return jsonify({"mensaje": "Error al registrar usuario"}), 500
    
@manejo_errores
def usu_eliminacion(uuid):
    # Valida la existencia del usuario a través del uuid 
    usuario = usuarios_services.obtener_usuario_por_uuid(uuid)

    if usuario:
        commit = usuarios_services.eliminar_usuario(uuid)
        if commit:
            return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200
    
        return jsonify({"mensaje": "Error al eliminar usuario"}), 500
    return jsonify({"mensaje": "El usuario no existe"}), 404

@manejo_errores
# Se valida de la misma manera que al registrar
def usu_actualizacion(uuid):
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["nombre", "username", "password_hash", "rol"])

    if validar_requeridos:
        return validar_requeridos
    
    nombre        = data['nombre']
    username      = data['username']
    password_hash = data['password_hash']
    rol           = data['rol']

    validar_datos = controllers.limpieza_datos(
        {"nombre": nombre, "usuario": username, "contraseña": password_hash, "rol": rol})

    if validar_datos:
        return validar_datos
    
    pass_encriptado = current_app.bcrypt.generate_password_hash(password_hash)

    usuario = usuarios_services.obtener_usuario_por_uuid(uuid)
    if usuario:
        try:
            commit = usuarios_services.actualizar_usuario(uuid.strip(), nombre.strip(), username, pass_encriptado, rol.strip().capitalize())
            return jsonify({"mensaje": "Usuario actualizado exitosamente"}), 200
        except ValueError as e:
            return jsonify({"mensaje": str(e)}), 400
        except Exception:
            return jsonify({"mensaje": "Error al actualizar usuario"}), 500
    return jsonify({"mensaje": "El usuario no existe"}), 404

@manejo_errores
def usu_pedidos_usuario(user):

    commit = usuarios_services.pedidos_de_un_usuario(user)
    if commit:
        return jsonify({"mensaje": "Usuario encontrado exitosamente",
                        "pedidos_por_usuario": commit}), 200
    
    return jsonify({"mensaje": "Error al buscar usuario"}), 500