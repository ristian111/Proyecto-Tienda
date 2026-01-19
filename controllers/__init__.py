from flask import jsonify
from .categorias_controller import cat_listado, cat_registro, cat_actualizacion, cat_eliminacion
from .auth_login_controllers import auth_login
from .clientes_controllers import cli_listado, cli_registro, cli_eliminacion, cli_actualizacion
from .detalle_pedido_controllers import det_pedido_actualizacion, det_pedido_eliminacion, det_pedido_listado, det_pedido_registro
from .facturas_controllers import fac_actualizacion, fac_listado, fac_eliminacion, fac_registro
from .inventarios_controllers import inv_actualizacion, inv_eliminacion, inv_listado, inv_listado_movimiento_inventario, inv_productos_stock_bajo, inv_registro, inv_stock_producto
from .pedidos_controllers import ped_actualizacion, ped_eliminacion, ped_listado, ped_listar_pedidos_pendientes, ped_registro
from .productos_controllers import prod_actualizacion, prod_eliminacion, prod_listado, prod_registro
from .reportes_controllers import rep_clientes_con_mas_pedidos, rep_ingresos_generados, rep_pedidos_por_fecha, rep_productos_mas_ganancias, rep_productos_mas_vendidos, rep_usuarios_con_mas_pedidos_registrados
from .usuarios_controllers import usu_actualizacion, usu_eliminacion, usu_listado, usu_pedidos_usuario, usu_registro

def validar_campos(datos: any, campos: list[str]):
   """
   Documentación para validar_campos
   
   Parametros: datos(type=any), campos(type=lista)

   Retorna un json con el codigo http 400
   """

   requeridos = campos
   faltantes  = [x for x in requeridos if x not in datos]

   if faltantes:
      return jsonify({"mensaje": f"Faltan los campos {", ".join(faltantes)}"}), 400
   
   return None