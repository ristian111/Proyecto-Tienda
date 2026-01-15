from models.reportes.reportes_models import ReporteBase

class PedidosPorFecha(ReporteBase):
    def __init__(self, resultado):
        super().__init__("pedidos_por_fecha", resultado)