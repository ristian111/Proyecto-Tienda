class Usuario:
    def __init__(self, id, uuid, nombre, user, password, rol, ultimo_acceso):
        self.id            = id
        self.uuid          = uuid
        self.nombre        = nombre
        self.rol           = rol
        self.ultimo_acceso = ultimo_acceso
        self.__user        = None
        self.__password    = None

    def usu_diccionario(self):
        return {
            'ref'          : self.uuid,
            'nombre'       : self.nombre,
            'user'         : self.__user,
            'password'     : self.__password,
            'rol'          : self.rol,
            'ultimo_acceso': self.ultimo_acceso
        }

    def get_usuario(self):
        return self.__user
    
    def get_contraseña(self):
        return self.__password

    def set_usuario(self, user):
        if len(user.strip()) < 10:
            return ValueError("El usuario debe tener al menos 10 caracteres")
        self.__user = user
    
    def set_contraseña(self, password):
        if len(password.strip()) < 10:
            return ValueError("La contraseña debe tener al menos 10 caracteres")
        self.__password = password