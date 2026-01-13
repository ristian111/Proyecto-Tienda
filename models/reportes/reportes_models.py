from abc import ABC, abstractmethod

class Reportes(ABC):
    def __init__(self, nombre, reporte):
        self.nombre_reporte    = nombre
        self.resultado_reporte = reporte

    @abstractmethod
    def ejecutar(self):
        pass

    @abstractmethod
    def rep_diccionario(self):
        pass