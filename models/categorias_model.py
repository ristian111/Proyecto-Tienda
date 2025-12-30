class Categoria:
    def __init__(self, id, uuid, nombre, descripcion):
        self.id          = id
        self.uuid        = uuid
        self.nombre      = nombre
        self.descripcion = descripcion

    def cat_diccionario(self):
        return {
            'ref'        : self.uuid,
            'nombre'     : self.nombre,
            'descripcion': self.descripcion
        }