from flask import current_app
from models import generar_token
from . import obtener_usuario_por_username

def autenticar_usuario(username, password):
    # Valida que el usuario exista y este autenticado
    usuario = obtener_usuario_por_username(username)

    if not usuario:
        return None
    
    # Relaciona la contraseña hash con la que contraseña que intento el usuario
    if not current_app.bcrypt.check_password_hash(
        usuario['password_hash'],
        password
    ):
        return None
    
    # Valida la creación del token mandando el usuario autenticado
    codificar_token = generar_token(usuario)

    if not codificar_token:
        return None
    
    return codificar_token