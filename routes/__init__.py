from .usuarios import usuarios_bp
from .facturas import facturas_bp
from .productos import productos_bp
from .categorias import categorias_bp
from .clientes import clientes_bp
from .inventarios import inventarios_bp
from .pedidos import pedidos_bp
from .swagger import swagger_bp

def cargarRutas(app):
    app.register_blueprint(swagger_bp, url_prefix='/swagger')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(facturas_bp, url_prefix='/facturas')
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(categorias_bp, url_prefix='/categorias')
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(inventarios_bp, url_prefix='/inventarios')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')