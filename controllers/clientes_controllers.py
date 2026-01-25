from flask import jsonify, request
from services import clientes_services
import controllers
from decoradores import manejo_errores

@manejo_errores
def cli_listado():
    # Devuelve en formato json el listado de clientes junto al codigo http 
    datos = clientes_services.listar_clientes()
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
    
    try:
        commit = clientes_services.registrar_clientes(nombre.strip(), telefono.strip(), direccion.strip())
        
        return jsonify({"mensaje": "Cliente registrado exitosamente",
                        "Cliente": commit}), 201
    except ValueError as e:
        return jsonify({"mensaje": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"mensaje": str(e)}), 500

@manejo_errores
def cli_eliminacion(uuid):
    # Valida la existencia del cliente a través del uuid 
    cliente = clientes_services.obtener_cliente_por_uuid(uuid)
    if cliente:
        commit = clientes_services.eliminar_cliente(uuid)
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
    
    cliente = clientes_services.obtener_cliente_por_uuid(uuid)
    if cliente:
    
        try:
            commit = clientes_services.actualizar_cliente(uuid.strip(), nombre.strip(), telefono.strip(), direccion.strip())
            return jsonify({"mensaje": "Cliente actualizado exitosamente",
                            "Cliente": commit}), 200
        except ValueError as e:
            return jsonify({"mensaje": str(e)}), 400
        except Exception as e:
            return jsonify({"mensaje": "Error al actualizar cliente"}), 500
    
    return jsonify({"mensaje": "El cliente no existe"}), 404