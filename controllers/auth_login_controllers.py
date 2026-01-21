from flask import request, jsonify
from services import auth_login_services
from decoradores import manejo_errores
import controllers

@manejo_errores
def auth_login():
    # Toma los datos del json dentro del cuerpo de la petición
    datos = request.get_json()

    # Valida que no existan campos vacios 
    validar_requeridos = controllers.validar_campos(datos, ["usuario", "contraseña"])

    if validar_requeridos:
        return validar_requeridos

    # Guarda los valores de la petición en variables
    usuario = datos['usuario']
    contraseña = datos['contraseña']

    # Valida que el usuario esta autenticado
    resultado = auth_login_services.autenticar_usuario(usuario, contraseña)

    if not resultado:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    return jsonify({"mensaje": "Token generado correctamente",
                    "token": resultado}), 200