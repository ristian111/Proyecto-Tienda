from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if not auth:
            return jsonify({"mensaje": "Token requerido"}), 401

        try:
            token = auth.split(" ")[1]
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )
            request.usuario = payload
        except:
            return jsonify({"mensaje": "Token inválido"}), 401

        return f(*args, **kwargs)
    return decorador
