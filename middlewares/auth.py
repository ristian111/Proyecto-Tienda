# Se utiliza la libreria functools para utilizar wraps para guardar los datos que maneja la funcion decorada asi como su nombre
from functools import wraps
from flask import request, jsonify, current_app
import jwt

# Recibe la función base
def token_requerido(f):
    # Retoma los datos de la funcion base
    @wraps(f)
    # Se implementa una restricción antes de que la funcion base se accione
    # *args, **kwargs Toma los argumentos de la funcion base llamada, ya sean posicionales o por nombre para que sirva con cualquier funcion
    def decorador(*args, **kwargs):

        # Accede al headers de la petición con el nombre 'Authorization'
        datos = request.headers.get('Authorization')

        # Valida si no hay header de 'Authorization'
        if not datos:
            return jsonify({"mensaje":"Ingreso no válido"}), 401
        
        # Valida que el token sea valido y no haya expirado
        try:
            # Separa los strings dentro de una lista evitando el 'Bearer' 
            token = datos.split(" ")[1]

            # Decodifica el token
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )

            # Guarda la petición del usuario para recordar sus datos (Luego se utiliza para la validación de roles)
            request.usuario = payload

        except jwt.InvalidTokenError:
            return jsonify({"mensaje": "Token inválido"}), 401
        except jwt.ExpiredSignatureError:
             return jsonify({"mensaje": "Token expirado"}), 401
        
        # Los parametros se reenvian a la funcion base sin ningun cambio
        return f(*args, **kwargs)
    return decorador