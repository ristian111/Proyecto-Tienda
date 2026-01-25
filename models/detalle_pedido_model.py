class DetallePedido:
    def __init__(self, id, uuid, cantidad, precio_unitario, subtotal, pedido_id, producto_id):
        self.id                = id
        self.uuid              = uuid
        self.subtotal          = subtotal
        self.pedido_id         = pedido_id
        self.producto_id       = producto_id
        self.__cantidad        = None
        self.__precio_unitario = None
        self.set_cantidad(cantidad)
        self.set_precio_unitario(precio_unitario)
    
    def det_ped_diccionario(self):
        return {
            'ref'            : self.uuid,
            'cantidad'       : self.__cantidad,
            'precio_unitario': self.__precio_unitario,
            'subtotal'       : self.subtotal,
            'ref_pedido'     : self.pedido_id,
            'ref_producto'   : self.producto_id,
        }
    
    def get_cantidad(self):
        return self.__cantidad
    
    def get_precio_unitario(self):
        return self.__precio_unitario
    
    def set_precio_unitario(self, precio_unitario):
        if precio_unitario <= 0:
            raise ValueError("El precio_unitario no puede ser negativo o igual a cero")
        self.__precio_unitario = precio_unitario
    
    def set_cantidad(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad no puede ser negativa o igual a cero")
        self.__cantidad = cantidad