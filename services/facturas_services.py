import uuid as uuidGenerado
from flask import current_app
from datetime import datetime
from MySQLdb.cursors import DictCursor
from models import Factura
from .utils_db import manejar_error_base_de_datos
from utils import errores

# Toma las filas de la base de datos utilizando inner join para ref_pedido donde luego se convierte en un diccionario 
def listar_facturas():
        
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT
                f.uuid as ref,
                f.numero_factura,
                f.total,
                f.fecha_emision,
                f.estado,
                ped.uuid as ref_pedido
            FROM facturas f 
            INNER JOIN pedidos ped on f.pedido_id = ped.id
        """
        cursor.execute(sql)
        return cursor.fetchall()
    
# Genera un uuid al momento de registrar y retorna un diccionario 
def registrar_factura(pedido_id, venta_presencial, pedido_uuid):

    conn = current_app.mysql.connection

    try:
        with conn.cursor(DictCursor) as cursor:
            conn.begin()

            #Calcular total de detalle_pedido
            sql_pedido = "SELECT SUM(subtotal) as total FROM detalle_pedido WHERE pedido_id = %s"
            cursor.execute(sql_pedido, (pedido_id,))
            datos = cursor.fetchone()

            if not datos or datos["total"] is None:
                raise errores.ErrorNegocio("El pedido no tiene detalle")

            total = datos["total"]

            #Actualizar total del pedido
            sql_actualizar_pedido = "UPDATE pedidos SET total = %s WHERE id = %s"
            cursor.execute(sql_actualizar_pedido, (total, pedido_id))

            #Validar stock
            sql_validar_stock = """
                SELECT 
                    i.producto_id, 
                    p.nombre, 
                    i.cantidad_actual,
                    i.cantidad_reservada,
                    dp.cantidad 
                FROM inventarios i 
                INNER JOIN productos p on i.producto_id = p.id
                INNER JOIN detalle_pedido dp on p.id = dp.producto_id
                WHERE dp.pedido_id = %s 
                AND i.cantidad_actual - i.cantidad_reservada < dp.cantidad
            """
            cursor.execute(sql_validar_stock, (pedido_id,))

            if cursor.fetchall():
                raise errores.ErrorNegocio("Stock insuficiente")

            #Insertar factura
            factura_uuid = str(uuidGenerado.uuid4())
            numero_factura = f"FAC-{datetime.now().strftime('%Y%m%d')}-{factura_uuid[:8]}"
            estado = "pagada" if venta_presencial else "emitida"

            sql_insertar_factura = """
                INSERT INTO facturas (uuid, numero_factura, total, estado, pedido_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insertar_factura, (factura_uuid, numero_factura, total, estado, pedido_id))
            factura_id = cursor.lastrowid

            #Actualizar inventario
            sql_actualizar_inventario = """
                UPDATE inventarios i INNER JOIN productos p on i.producto_id = p.id 
                INNER JOIN detalle_pedido dp on p.id = dp.producto_id

                SET i.cantidad_actual = i.cantidad_actual - dp.cantidad
                WHERE dp.pedido_id = %s
            """
            cursor.execute(sql_actualizar_inventario, (pedido_id,))

            #Actualizar estado del pedido
            sql_actualizar_estado_pedido = "UPDATE pedidos SET estado = %s WHERE id = %s"
            cursor.execute(sql_actualizar_estado_pedido, ("entregado" if not venta_presencial else "pendiente", pedido_id))

            conn.commit()

            fecha_emision = datetime.now()
            resultado = Factura(factura_id, factura_uuid, numero_factura, total, fecha_emision, estado, pedido_uuid).fac_diccionario()
            return resultado
    
    except Exception as e:
        conn.rollback()
        manejar_error_base_de_datos(e, "factura", "registrar", "No puede haber dos facturas para este pedido")

# Utiliza uuid para acceder a la factura y retorna True o False si modifico la factura
def actualizar_factura(uuid, numero_factura, total, estado, pedido_id, pedido_uuid):
    
    try:
        factura = Factura(None, uuid, numero_factura, total, datetime.now().isoformat(), estado, pedido_uuid)
        
        with current_app.mysql.connection.cursor() as cursor:
            sql = "UPDATE facturas SET numero_factura=%s, total=%s, estado=%s, pedido_id=%s WHERE uuid = %s"
            cursor.execute(sql,(numero_factura, total, estado, pedido_id, uuid))
            current_app.mysql.connection.commit()
            return factura.fac_diccionario()
        
    except Exception as e:
        current_app.mysql.connection.rollback()
        manejar_error_base_de_datos(e, "factura", "registrar", "No puede haber dos facturas para este pedido") 

def eliminar_factura(uuid):

    try:
        with current_app.mysql.connection.cursor() as cursor:
            sql = "DELETE FROM facturas WHERE uuid = %s"
            cursor.execute(sql,(uuid,))
            current_app.mysql.connection.commit()
            return cursor.rowcount > 0
        
    except Exception:
        current_app.mysql.connection.rollback()
        raise 

# Devuelve en forma de diccionario la fila de la factura para su uso en la validación de las demas tablas
def obtener_factura_por_uuid(uuid):

    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = "SELECT * FROM facturas WHERE uuid = %s"
        cursor.execute(sql,(uuid,))
        return cursor.fetchone()
        