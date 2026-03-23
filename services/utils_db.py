from utils import errores
from MySQLdb import IntegrityError
from flask import current_app

def manejar_error_base_de_datos(error: any, servicio: str, accion: str, duplicado=None, conn=None): 
    
   """
   Documentación para manejar_error_base_de_datos
   
   :param error: Debe ingresar como argumento la instancia del error Exception en la capa services
   :type error: any
   :param servicio: Debe ingresar como argumento el nombre del servicio
   :type servicio: str
   :param accion: Debe ingresar como argumento la acción del servicio
   :type accion: str
   :param duplicado: Debe ingresar como argumento que servicio duplica
   :type duplicado: str

   ¿Qué hace?: Centraliza los errores de la base de datos, como restricciones

   Retorna un error personalizado
   """
   
   if conn:
        conn.rollback()
   else:
        current_app.mysql.connection.rollback()
   
   if isinstance(error, errores.ErrorNegocio):
       raise error
   
   if isinstance(error, IntegrityError):
        
        codigo_error = error.args[0]

        if codigo_error == 1062 and duplicado:
            raise errores.ErrorDuplicado(duplicado)
        
        raise RuntimeError(f"Error de integridad de datos al {accion} {servicio}") from error
        
   raise errores.ErrorBaseDatos(f"Error interno al {accion} {servicio}") from error