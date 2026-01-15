class ReporteBase:
    def __init__(self, nombre, reporte):
        self.nombre_reporte    = nombre
        self.resultado_reporte = reporte

    def rep_diccionario(self):
        return {
            "nombre_reporte": self.nombre_reporte,
            "resultados"    : self.resultado_reporte
        }