class ErrorNegocio(Exception):
    """Errores de lógica: stock, campos inválidos, etc."""
    pass

class ErrorDuplicado(Exception):
    """Específico para el error 1062 de MySQL."""
    pass

class ErrorBaseDatos(Exception):
    """Para errores técnicos de SQL que no son culpa del usuario."""
    pass