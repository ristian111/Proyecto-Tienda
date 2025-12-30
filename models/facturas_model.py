class Factura:
    def __init__(self, id, uuid, numero_factura, total, fecha_emision, estado, pedido_uuid):
        self.id             = id
        self.uuid           = uuid
        self.numero_factura = numero_factura
        self.total          = total
        self.fecha_emision  = fecha_emision
        self.estado         = estado
        self.pedido_uuid    = pedido_uuid

    def fac_diccionario(self):
        return {
            'ref'           : self.uuid,
            'numero_factura': self.numero_factura,
            'total'         : self.total,
            'fecha_emision' : self.fecha_emision,
            'estado'        : self.estado,
            'ref_pedido'    : self.pedido_uuid,
        }