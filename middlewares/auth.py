from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        datos = request.headers.get('Authorization')

        if not datos:
            return jsonify({"mensaje":"Ingreso no válido"}), 401
        
        try:
            token = datos.split(" ")[1]

            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )

            request.usuario = payload

        except jwt.InvalidTokenError:
            return jsonify({"mensaje": "Token inválido"}), 401
        except jwt.ExpiredSignatureError:
             return jsonify({"mensaje": "Token expirado"}), 401

        return f(*args, **kwargs)
    return decorador