from flask import request, jsonify
from services.auth_login_services import autenticar_usuario

def auth_login():
    datos = request.get_json()

    requeridos = ["username", "password"]
    faltantes  = [x for x in requeridos if x not in datos]

    if faltantes:
        return jsonify({"mensaje": "Los campos no pueden estar vacíos"}), 400
    
    username = datos['username']
    password = datos['password']

    resultado = autenticar_usuario(username, password)

    if not resultado:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    
    return jsonify(resultado), 200