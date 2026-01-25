class Producto:
    def __init__(self, id, uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_uuid):
        self.id              = id
        self.uuid            = uuid
        self.nombre          = nombre
        self.unidad_medida   = unidad_medida
        self.categoria_uuid  = categoria_uuid
        self.__precio_venta  = None
        self.__precio_compra = None
        self.set_precio_compra(precio_compra)
        self.set_precio_venta(precio_venta)
    
    def prod_diccionario(self):
        return {
            'ref'           : self.uuid,
            'nombre'        : self.nombre,
            'precio_venta'  : self.__precio_venta,
            'precio_compra' : self.__precio_compra,
            'unidad_medida' : self.unidad_medida,
            'ref_categoria' : self.categoria_uuid
        }
    
    def get_precio_venta(self):
        return self.__precio_venta
    
    def get_precio_compra(self):
        return self.__precio_compra
    
    def set_precio_compra(self, precio_compra):
        if precio_compra < 0:
            raise ValueError("precio_compra no puede ser negativa")
        self.__precio_compra = precio_compra

    def set_precio_venta(self, precio_venta):
        if precio_venta < 0 or precio_venta < self.__precio_compra:
            raise ValueError("precio_venta no puede ser negativa ni puede ser menor al precio_compra")
        self.__precio_venta = precio_venta