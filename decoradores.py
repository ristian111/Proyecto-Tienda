from functools import wraps
from flask import jsonify

def manejo_errores(f):
   @wraps(f)
   def decorador(*args, **kwargs):
      try:
         return f(*args, **kwargs)
      except Exception as e:
         print(str(e))
         return jsonify({"Error interno del servidor"}), 500
   return decorador