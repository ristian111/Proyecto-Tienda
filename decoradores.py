from functools import wraps
from flask import jsonify
from utils import errores 

def manejo_errores(f):
   @wraps(f)
   def decorador(*args, **kwargs):
      try:
         return f(*args, **kwargs)
      except errores.ErrorNegocio as e:
         return jsonify({"mensaje": str(e)}), 400
      except errores.ErrorDuplicado as e:
         return jsonify({"mensaje": str(e)}), 409
      except errores.ErrorBaseDatos as e:
         print(e.__cause__) 
         return jsonify({"mensaje": str(e)}), 500
      except RuntimeError as e:
         return jsonify({"mensaje": str(e)}), 500
      except Exception as e:
         return jsonify({"mensaje": "Error interno del servidor"}), 500
   return decorador