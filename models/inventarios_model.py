class Inventario:
    def __init__(self, id, uuid, producto_uuid, cantidad_actual, cantidad_reservada, punto_reorden, ultima_actualizacion):
        self.id                   = id
        self.uuid                 = uuid
        self.producto_uuid        = producto_uuid
        self.cantidad_actual      = cantidad_actual
        self.cantidad_reservada   = cantidad_reservada
        self.punto_reorden        = punto_reorden
        self.ultima_actualizacion = ultima_actualizacion

    def inv_diccionario(self):
        return {
            'ref'                 : self.uuid,
            'ref_producto'        : self.producto_uuid,
            'cantidad_actual'     : self.cantidad_actual,
            'cantidad_reservada'  : self.cantidad_reservada,
            'punto_reorden'       : self.punto_reorden,
            'ultima_actualizacion': self.ultima_actualizacion
        }