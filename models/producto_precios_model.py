from utils import errores

class ProductoPrecio:
    def __init__(self, id, uuid, producto_id, precio_compra, precio_venta, vigente_desde, vigente_hasta, activo):
        self.id             = id
        self.uuid           = uuid
        self.producto_id    = producto_id
        self.precio_compra  = precio_compra
        self.precio_venta   = precio_venta
        self.vigente_desde  = vigente_desde
        self.vigente_hasta  = vigente_hasta
        self.activo         = activo

        self.validar()

    def validar(self):
        if self.precio_compra < 0 or self.precio_venta < 0:
            raise errores.ErrorNegocio("Los precios no pueden ser negativos")
        if self.precio_venta < self.precio_compra:
            raise errores.ErrorNegocio("El precio de venta no puede ser menor al precio de compra")

    def to_dict(self):
        return {
            "ref"           : self.uuid,
            "producto_id"   : self.producto_id,
            "precio_compra" : self.precio_compra,
            "precio_venta"  : self.precio_venta,
            "vigente_desde" : self.vigente_desde,
            "vigente_hasta" : self.vigente_hasta,
            "activo"        : self.activo
        }
