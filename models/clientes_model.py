class Cliente:
    def __init__(self, id, uuid, nombre, telefono, direccion):
        self.id        = id
        self.uuid      = uuid
        self.nombre    = nombre
        self.telefono  = telefono
        self.direccion = direccion

    def cli_diccionario(self):
        return {
            'ref'      : self.uuid,
            'nombre'   : self.nombre,
            'telefono' : self.telefono,
            'direccion': self.direccion
        }