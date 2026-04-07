from utils import errores

class Producto:
    def __init__(self, id, uuid, nombre, precio_venta, costo_promedio, unidad_medida, categoria_uuid):
        self.id              = id
        self.uuid            = uuid
        self.nombre          = nombre
        self.unidad_medida   = unidad_medida
        self.categoria_uuid  = categoria_uuid
        self.__precio_venta  = None
        self.__costo_promedio = None
        self.set_costo_promedio(costo_promedio)
        self.set_precio_venta(precio_venta)
    
    def prod_diccionario(self):
        return {
            'ref'           : self.uuid,
            'nombre'        : self.nombre,
            'precio_venta'  : self.__precio_venta,
            'costo_promedio': self.__costo_promedio,
            'unidad_medida' : self.unidad_medida,
            'ref_categoria' : self.categoria_uuid
        }
    
    def get_precio_venta(self):
        return self.__precio_venta
    
    def get_costo_promedio(self):
        return self.__costo_promedio
    
    def set_costo_promedio(self, costo_promedio):
        # We can allow costo_promedio to be None if needed, but here assuming >= 0
        if costo_promedio is not None and costo_promedio < 0:
            raise errores.ErrorNegocio("El costo promedio no puede ser negativo")
        self.__costo_promedio = costo_promedio

    def set_precio_venta(self, precio_venta):
        if precio_venta < 0 or (self.__costo_promedio is not None and precio_venta < self.__costo_promedio):
            raise errores.ErrorNegocio("El precio de venta no puede ser negativo ni puede ser menor al costo promedio")
        self.__precio_venta = precio_venta