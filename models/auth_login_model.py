import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

# A través del usuario autenticado se genera el token
def generar_token(usuario):
    # Define el token para luego codificarlo y generarlo
    payload = {
        "uuid": usuario["uuid"],
        "rol": usuario["rol"],
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return token
