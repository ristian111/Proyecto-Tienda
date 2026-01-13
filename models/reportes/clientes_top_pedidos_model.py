from models.reportes.reportes_models import Reportes

class ClienteTopPedidosReporte(Reportes):
    def __init__(self, resultados):
        super().__init__("clientes_con_mas_pedidos", resultados)

    def ejecutar(self):
        return self.resultado_reporte

    def rep_diccionario(self):
        return {
            'Nombre reporte'   : self.nombre_reporte,
            'Resultados'       : self.resultado_reporte
        }
