from models.reportes.reportes_models import ReporteBase

class Ingresos(ReporteBase):
    def __init__(self, resultado):
        super().__init__("ingresos_de_ventas", resultado)