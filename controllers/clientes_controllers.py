from flask import jsonify, request
from services import clientes_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def cli_listado():
    uuid_usuario = request.usuario['uuid']
    datos = clientes_services.listar_clientes(uuid_usuario)
    return jsonify(datos), 200

@manejo_errores
def cli_registro():
    # Valida que no existan campos vacios 
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["nombre", "telefono", "direccion"])

    if validar_requeridos:
        return validar_requeridos
    
    # Guarda los valores de la petición en variables
    nombre    = data['nombre']
    telefono  = data['telefono']
    direccion = data['direccion']

    # Valida que los datos sean de la clase adecuada o si el campo lo rellenan con un espacio 
    validar_datos = controllers.limpieza_datos({"nombre": nombre, "telefono": telefono, "direccion": direccion})

    if validar_datos:
        return validar_datos
    
    uuid_usuario = request.usuario['uuid']
    commit = clientes_services.registrar_clientes(nombre.strip(), telefono.strip(), direccion.strip(), uuid_usuario)
    
    return jsonify({"mensaje": "Cliente registrado exitosamente",
                    "Cliente": commit}), 201


@manejo_errores
def cli_eliminacion(uuid):
    uuid_usuario = request.usuario['uuid']
    # Valida la existencia del cliente a través del uuid 
    cliente = clientes_services.obtener_cliente_por_uuid(uuid, uuid_usuario)
    if cliente:
        commit = clientes_services.eliminar_cliente(uuid, uuid_usuario)
        if commit:
            return jsonify({"mensaje": "Cliente eliminado exitosamente"}), 200
        
        return jsonify({"mensaje": "Error al eliminar cliente"}), 500
    return jsonify({"mensaje": "El cliente no existe"}), 404

@manejo_errores
# Se valida de la misma manera que al registrar
def cli_actualizacion(uuid):
    data = request.get_json()

    validar_requeridos = controllers.validar_campos(data, ["nombre", "telefono", "direccion"])

    if validar_requeridos:
        return validar_requeridos
    
    nombre    = data['nombre']
    telefono  = data['telefono']
    direccion = data['direccion']

    validar_datos = controllers.limpieza_datos({"nombre": nombre, "telefono": telefono, "direccion": direccion})

    if validar_datos:
        return validar_datos
    
    uuid_usuario = request.usuario['uuid']
    cliente = clientes_services.obtener_cliente_por_uuid(uuid, uuid_usuario)
    if cliente:
    
        commit = clientes_services.actualizar_cliente(uuid.strip(), nombre.strip(), telefono.strip(), direccion.strip(), uuid_usuario)
        return jsonify({"mensaje": "Cliente actualizado exitosamente",
                        "Cliente": commit}), 200
    
    return jsonify({"mensaje": "El cliente no existe"}), 404