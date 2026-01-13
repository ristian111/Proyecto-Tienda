from models.reportes.reportes_models import Reportes

class UsuariosTopRegistrosPedidos(Reportes):
    def __init__(self, resultados):
        super().__init__("usuarios_con_mas_pedidos_registrados", resultados)
    
    def ejecutar(self):
        return self.resultado_reporte
    
    def rep_diccionario(self):
        return {
            'Reporte'          : self.nombre_reporte,
            'Resultados'       : self.resultado_reporte
        }