from .usuarios import usuarios_bp
from .facturas import facturas_bp
from .productos import productos_bp
from .categorias import categorias_bp
from .clientes import clientes_bp
from .inventarios import inventarios_bp
from .pedidos import pedidos_bp
from .detalle_pedido import detalle_pedido_bp
from .auth_login import auth_login_bp
from ..swagger import swagger_bp
from .reportes import reportes_bp

def cargarRutas_v1(app):
    app.register_blueprint(reportes_bp, url_prefix='/v1/reportes')
    app.register_blueprint(swagger_bp, url_prefix='/swagger')
    app.register_blueprint(auth_login_bp, url_prefix='/v1/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/v1/usuarios')
    app.register_blueprint(facturas_bp, url_prefix='/v1/facturas')
    app.register_blueprint(productos_bp, url_prefix='/v1/productos')
    app.register_blueprint(categorias_bp, url_prefix='/v1/categorias')
    app.register_blueprint(clientes_bp, url_prefix='/v1/clientes')
    app.register_blueprint(inventarios_bp, url_prefix='/v1/inventarios')
    app.register_blueprint(pedidos_bp, url_prefix='/v1/pedidos')
    app.register_blueprint(detalle_pedido_bp, url_prefix="/v1/detalles")