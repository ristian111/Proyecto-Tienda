from flask import current_app
from models import DetallePedido
import uuid as uuidGenerado
from MySQLdb.cursors import DictCursor

# Toma las filas de la base de datos para convertirlas en un diccionario 
def listar_detalles_pedidos():
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """
            SELECT
                det.id,
                det.uuid,
                det.cantidad,
                det.precio_unitario,
                det.subtotal,
                ped.uuid as ref_pedido,
                prod.uuid as ref_producto
            FROM detalle_pedido det
            INNER JOIN pedidos ped on det.pedido_id = ped.id
            INNER JOIN productos prod on det.producto_id = prod.id
        """
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [DetallePedido(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).det_ped_diccionario() for x in datos]
        return resultado
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

# Genera un uuid al momento de registrar y retorna un diccionario 
def registrar_detalle_pedido(cantidad, precio_unitario, pedido_id, producto_id):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        uuid = str(uuidGenerado.uuid4())
        sql = "INSERT INTO detalle_pedido (uuid, cantidad, precio_unitario, pedido_id, producto_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (uuid, cantidad, precio_unitario, pedido_id, producto_id))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid
        return DetallePedido(id, uuid, cantidad, precio_unitario, None, pedido_id, producto_id).det_ped_diccionario()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

# Utiliza uuid para acceder al detalle_pedido y retorna True o False si modifico el detalle_pedido
def actualizar_detalle_pedido(uuid, cantidad, precio_unitario, pedido_id, producto_id):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "UPDATE detalle_pedido SET cantidad=%s, precio_unitario=%s, pedido_id=%s, producto_id=%s WHERE uuid=%s"
        cursor.execute(sql, (cantidad, precio_unitario, pedido_id, producto_id, uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
       
def eliminar_detalle_pedido(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "DELETE FROM detalle_pedido WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

# Devuelve en forma de diccionario la fila del detalle_pedido para su uso en la validación de las demas tablas
def obtener_detalle_pedido_por_uuid(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM detalle_pedido WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()