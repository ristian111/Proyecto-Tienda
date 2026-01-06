from flask import request, jsonify
from services.auth_login_services import autenticar_usuario

def auth_login():

    # Toma los datos del json dentro del cuerpo de la petición
    datos = request.get_json()

    # Valida que no existan campos vacios 
    requeridos = ["username", "password"]
    faltantes  = [x for x in requeridos if x not in datos]

    if faltantes:
        return jsonify({"mensaje": "Los campos no pueden estar vacíos"}), 400
    
    # Guarda los valores de la petición en variables
    username = datos['username']
    password = datos['password']

    # Valida que el usuario esta autenticado
    resultado = autenticar_usuario(username, password)

    if not resultado:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    
    return jsonify({"mensaje": "Token generado correctamente",
                    "token": resultado}), 200