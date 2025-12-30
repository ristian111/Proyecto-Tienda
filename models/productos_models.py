class Producto:
    def __init__(self, id, uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_uuid):
        self.id              = id
        self.uuid            = uuid
        self.nombre          = nombre
        self.precio_venta    = precio_venta
        self.precio_compra   = precio_compra
        self.unidad_medida   = unidad_medida
        self.categoria_uuid  = categoria_uuid
    
    def prod_diccionario(self):
        return {
            'ref'           : self.uuid,
            'nombre'        : self.nombre,
            'precio_venta'  : self.precio_venta,
            'precio_compra' : self.precio_compra,
            'unidad_medida' : self.unidad_medida,
            'ref_categoria' : self.categoria_uuid
        }