# Se utiliza la libreria functools para utilizar wraps para guardar los datos que maneja la funcion decorada asi como su nombre
from functools import wraps
from flask import request, jsonify, current_app

# Recibe la función base
def api_key_requerido(f):
    # Retoma los datos de la funcion base
    @wraps(f)
    # Se implementa una restricción antes de que la funcion base se accione
    # *args, **kwargs Toma los argumentos de la funcion base llamada, ya sean posicionales o por nombre para que sirva con cualquier funcion
    def decorated(*args, **kwargs):

        # Accede al headers de la petición con el nombre 'Authorization'
        api_key = request.headers.get('Authorization')

        # Valida si no hay header de 'Authorization' o si no coincide con la 'API_KEY' configurada
        if not api_key or api_key != current_app.config['API_KEY']:
            return jsonify({"mensaje": "API Key inválida o ausente"}), 401
        
        # Los parametros se reenvian a la funcion base sin ningun cambio
        return f(*args, **kwargs)
    
    return decorated
