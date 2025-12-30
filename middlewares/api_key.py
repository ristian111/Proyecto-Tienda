from functools import wraps
from flask import request, jsonify, current_app

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('Authorization')

        if not api_key or api_key != current_app.config['API_KEY']:
            return jsonify({"mensaje": "API Key inválida o ausente"}), 401

        return f(*args, **kwargs)
    return decorated
