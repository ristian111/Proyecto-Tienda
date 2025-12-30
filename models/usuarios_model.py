class Usuario:
    def __init__(self, id, uuid, nombre, user, password, rol, ultimo_acceso):
        self.id            = id
        self.uuid          = uuid
        self.nombre        = nombre
        self.user          = user
        self.password      = password
        self.rol           = rol
        self.ultimo_acceso = ultimo_acceso

    def usu_diccionario(self):
        return {
            'ref'          : self.uuid,
            'nombre'       : self.nombre,
            'user'         : self.user,
            'password'     : self.password,
            'rol'          : self.rol,
            'ultimo_acceso': self.ultimo_acceso
        }
    
