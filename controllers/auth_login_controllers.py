from flask import request, jsonify
from services.auth_login_services import autenticar_usuario

def auth_login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"mensaje": "Datos incompletos"}), 400

    resultado = autenticar_usuario(
        data["username"],
        data["password"]
    )

    if not resultado:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    return jsonify(resultado), 200
