import jwt
from datetime import datetime, timedelta
from flask import current_app

def generar_token(usuario):
    payload = {
        "uuid": usuario["uuid"],
        "rol": usuario["rol"],
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return token
