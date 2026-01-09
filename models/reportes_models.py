class ClientePedidosReporte:
    def __init__(self, nombre, numero_pedidos):
        self.nombre = nombre
        self.numero_pedidos = numero_pedidos

    def clientes_con_mas_pedidos(self):
        return {
            'cliente': self.nombre,
            'numero_pedidos': self.numero_pedidos
        }
