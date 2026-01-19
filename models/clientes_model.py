class Cliente:
    def __init__(self, id, uuid, nombre, telefono, direccion):
        self.id         = id
        self.uuid       = uuid
        self.nombre     = nombre
        self.direccion  = direccion
        self.__telefono = None
        self.set_telefono(telefono)

    def cli_diccionario(self):
        return {
            'ref'      : self.uuid,
            'nombre'   : self.nombre,
            'telefono' : self.__telefono,
            'direccion': self.direccion
        }
    
    def get_telefono(self):
        return self.__telefono
    
    def set_telefono(self, telefono):
        if len(telefono) == 10:
            self.__telefono = telefono
        else:
            raise ValueError("El teléfono debe tener 10 carácteres")