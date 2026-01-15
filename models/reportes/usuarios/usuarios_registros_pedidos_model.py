from models.reportes.reportes_models import ReporteBase

class UsuariosMasRegistrosPedidos(ReporteBase):
    def __init__(self, resultados):
        super().__init__("usuarios_con_mas_pedidos_registrados", resultados)