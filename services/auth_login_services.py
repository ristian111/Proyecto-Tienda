from flask import current_app
from models import auth_login_model
from services import usuarios_services

def autenticar_usuario(usuario, contraseña):
    # Valida que el usuario exista y este autenticado
    usuario_existente = usuarios_services.obtener_usuario_por_username(usuario)

    if not usuario_existente:
        return None
    
    # Relaciona la contraseña hash con la que contraseña que intento el usuario
    if not current_app.bcrypt.check_password_hash(
        usuario_existente['password_hash'],
        contraseña
    ):
        return None
    
    # Valida la creación del token mandando el usuario autenticado
    codificar_token = auth_login_model.generar_token(usuario_existente)

    if not codificar_token:
        return None
    
    return codificar_token