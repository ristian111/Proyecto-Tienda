from models.reportes.reportes_models import ReporteBase

class ClientesMasPedidos(ReporteBase):
    def __init__(self, resultados):
        super().__init__("clientes_con_mas_pedidos", resultados)