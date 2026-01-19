class DetallePedido:
    def __init__(self, id, uuid, cantidad, precio_unitario, subtotal, pedido_id, producto_id):
        self.id              = id
        self.uuid            = uuid
        self.__cantidad      = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal        = subtotal
        self.pedido_id       = pedido_id
        self.producto_id     = producto_id
    
    def det_ped_diccionario(self):
        return {
            'ref'            : self.uuid,
            'cantidad'       : self.__cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal'       : self.subtotal,
            'ref_pedido'     : self.pedido_id,
            'ref_producto'   : self.producto_id,
        }
    
    def get_cantidad(self):
        return self.__cantidad