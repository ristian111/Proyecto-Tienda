from flask import current_app
from datetime import datetime, timedelta
import jwt
from services.usuarios_services import obtener_usuario_por_username

def autenticar_usuario(username, password):
    usuario = obtener_usuario_por_username(username)

    if not usuario:
        return None
    
    if not current_app.bcrypt.check_password_hash(
        usuario['password_hash'],
        password
    ):
        return None
    
    payload = {
        'uuid': usuario['uuid'],
        'rol' : usuario['rol'],
        'exp' : datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return token