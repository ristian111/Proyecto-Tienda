# Se utiliza la libreria functools para utilizar wraps para guardar los datos que maneja la funcion decorada asi como su nombre
from flask import request
from functools import wraps

# Recibe el argumento del decorador (Admin, Tendero)
def rol_requerido(rol):
    # Recibe la función base
    def decorador(f):
        # Retoma los datos de la funcion base
        @wraps(f)
        # Se implementa una restricción antes de que la funcion base se accione
        # *args, **kwargs Toma los argumentos de la funcion base llamada, ya sean posicionales o por nombre para que sirva con cualquier funcion
        def wrapper(*args, **kwargs):

            # Accede a la petición por medio del atributo creado de usuario al rol del usuario y verifica su rol
            if request.usuario.get("rol") != rol:
                return {"mensaje": "Acceso denegado"}, 403
            
            # Los parametros se reenvian a la funcion base sin ningun cambio
            return f(*args, **kwargs)
        return wrapper
    return decorador