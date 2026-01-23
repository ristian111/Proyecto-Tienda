class Pedido:
    def __init__(self, id, uuid, estado, total, direccion_entrega, fecha_hora, nombre_ciente, cliente_id, usuario_id):
        self.id                = id
        self.uuid              = uuid
        self.estado            = estado
        self.total             = total
        self.direccion_entrega = direccion_entrega
        self.fecha_hora        = fecha_hora
        self.nombre_ciente     = nombre_ciente
        self.cliente_id        = cliente_id
        self.usuario_id        = usuario_id
    
    def ped_diccionario(self):
        return {
            'ref'              : self.uuid,
            'cliente'          : self.nombre_ciente,
            'estado'           : self.estado,
            'total'            : self.total,
            'direccion_entrega': self.direccion_entrega,
            'fecha_hora'       : self.fecha_hora,
            'ref_cliente'      : self.cliente_id,
            'ref_usuario'      : self.usuario_id
        }