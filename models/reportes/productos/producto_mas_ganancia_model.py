from models.reportes.reportes_models import ReporteBase

class ProductosMasGanancia(ReporteBase):
    def __init__(self, resultado):
        super().__init__("producto_con_mas_ganancia", resultado)