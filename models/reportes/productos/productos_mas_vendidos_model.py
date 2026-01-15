from models.reportes.reportes_models import ReporteBase

class ProductosMasVendidos(ReporteBase):
    def __init__(self, resultados):
        super().__init__("productos_mas_vendidos", resultados)