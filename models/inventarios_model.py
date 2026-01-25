class Inventario:
    def __init__(self, id, uuid, producto_uuid, cantidad_actual, cantidad_reservada, punto_reorden, ultima_actualizacion):
        self.id                   = id
        self.uuid                 = uuid
        self.producto_uuid        = producto_uuid
        self.ultima_actualizacion = ultima_actualizacion
        self.__cantidad_actual    = None
        self.__cantidad_reservada = None
        self.__punto_reorden      = None
        self.set_cantidad_actual(cantidad_actual)
        self.set_cantidad_reservada(cantidad_reservada)
        self.set_punto_reorden(punto_reorden)

    def inv_diccionario(self):
        return {
            'ref'                 : self.uuid,
            'ref_producto'        : self.producto_uuid,
            'cantidad_actual'     : self.__cantidad_actual,
            'cantidad_reservada'  : self.__cantidad_reservada,
            'punto_reorden'       : self.__punto_reorden,
            'ultima_actualizacion': self.ultima_actualizacion
        }
    
    def get_cantidad_actual(self):
        return self.__cantidad_actual
    
    def get_cantidad_reservada(self):
        return self.__cantidad_reservada
    
    def get_punto_reorden(self):
        return self.__punto_reorden
    
    def set_cantidad_actual(self, cantidad_actual):
        if cantidad_actual < 0:
            raise ValueError("cantidad_actual no puede ser negativa")
        self.__cantidad_actual = cantidad_actual
    
    def set_cantidad_reservada(self, cantidad_reservada):
        if cantidad_reservada < 0 or cantidad_reservada > self.__cantidad_actual:
            raise ValueError("cantidad_reservada no puede ser negativa ni puede ser mayor que cantidad_actual")
        self.__cantidad_reservada = cantidad_reservada
    
    def set_punto_reorden(self, punto_reorden):
        if punto_reorden < 0:
            raise ValueError("punto_reorden no puede ser negativo")
        self.__punto_reorden = punto_reorden

class MovimientoInventario:
    def __init__(self, id, producto_id_ant, cantidad_actual_ant, cantidad_reservada_ant, 
                 punto_reorden_ant, producto_id_nue, cantidad_actual_nue, cantidad_reservada_nue, 
                 punto_reorden_nue, accion, fecha_hora, usuario_id):
        
        self.id                     = id
        self.producto_id_ant        = producto_id_ant
        self.cantidad_actual_ant    = cantidad_actual_ant
        self.cantidad_reservada_ant = cantidad_reservada_ant
        self.punto_reorden_ant      = punto_reorden_ant
        self.producto_id_nue        = producto_id_nue
        self.cantidad_actual_nue    = cantidad_actual_nue
        self.cantidad_reservada_nue = cantidad_reservada_nue
        self.punto_reorden_nue      = punto_reorden_nue
        self.accion                 = accion
        self.fecha_hora             = fecha_hora
        self.usuario_id             = usuario_id
    
    def mov_inv_diccionario(self):
        return {
            'cantidad_actual_ant'   : self.cantidad_actual_ant,
            'cantidad_reservada_ant': self.cantidad_reservada_ant,
            'punto_reorden_ant'     : self.punto_reorden_ant,
            'cantidad_actual_nue'   : self.cantidad_actual_nue,
            'cantidad_reservada_nue': self.cantidad_reservada_nue,
            'punto_reorden_nue'     : self.punto_reorden_nue,
            'accion'                : self.accion,
            'fecha_hora'            : self.fecha_hora,
            'ref_usuario'           : self.usuario_id
        }