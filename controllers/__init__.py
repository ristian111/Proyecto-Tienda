from . import categorias_controller
from . import auth_login_controllers 
from . import clientes_controllers
from . import detalle_pedido_controllers
from . import facturas_controllers
from . import inventarios_controllers
from . import pedidos_controllers
from . import productos_controllers 
from . import reportes_controllers 
from . import usuarios_controllers
from flask import jsonify

def validar_campos(datos: any, requeridos: list[str]):
   """
   Documentación para validar_campos
   
   :param datos: Debe ingresar como argumento los datos json del request
   :type datos: any
   :param requeridos: Debe ingresar como argumento los campos requeridos
   :type requeridos: list[str]

   ¿Qué hace?: Valida que los campos requeridos si esten 

   Retorna un json con el codigo http 400 o None
   """

   faltantes  = [x for x in requeridos if x not in datos]

   if faltantes:
      return jsonify({"mensaje": f"Faltan los campos {", ".join(faltantes)}"}), 400
   
   return None

def limpieza_datos(campos: dict):
   """
   Documentación para limpieza_datos
   
   :param campo: Debe ingresar como argumento un campo para su limpieza
   :type campo: dict

   ¿Qué hace?: Valida si es string o el campo esta vacío

   Retorna un json con el codigo http 400 o None
   """

   validar_limpieza = [campo for campo, valor in campos.items() if not isinstance(valor, str) or not valor.strip()]
   
   if validar_limpieza:
      return jsonify({"mensaje": 
                      f"Los campos {(", ".join(validar_limpieza))} deben ser una cadena de texto o no pueden estar vacíos"}), 400
   
   return None