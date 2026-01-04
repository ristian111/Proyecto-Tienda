from flask import request
from functools import wraps

def rol_requerido(rol):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.usuario.get("rol") != rol:
                return {"mensaje": "Acceso denegado"}, 403
            return f(*args, **kwargs)
        return wrapper
    return decorador