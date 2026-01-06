from flask import Blueprint
from controllers.auth_login_controllers import auth_login

auth_login_bp = Blueprint("auth", __name__)

@auth_login_bp.route("/login", methods=['POST'])
def login():
    datos = auth_login()
    return datos