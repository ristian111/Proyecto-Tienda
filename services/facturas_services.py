from flask import current_app
import uuid as uuidGenerado
from MySQLdb.cursors import DictCursor
from models.facturas_model import Factura

def listar_facturas():
    facturas = current_app.mysql.connection.cursor()
    sql = """
        SELECT
            f.id,
            f.uuid,
            f.numero_factura,
            f.total,
            f.fecha_emision,
            f.estado,
            ped.uuid
        FROM facturas f INNER JOIN pedidos p on f.pedido_id = ped.id
    """
    facturas.execute(sql)
    datos = facturas.fetchall()
    resultado = [Factura(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).fac_diccionario() for x in datos]
    return resultado

def registrar_factura(numero_factura, total, estado, pedido_uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        uuid = str(uuidGenerado.uuid4())
        sql = "INSERT INTO facturas (uuid, numero_factura, total, estado, pedido_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql,(uuid, numero_factura, total, estado, pedido_uuid))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid
        return Factura(id, uuid, numero_factura, total, None, estado, pedido_uuid).fac_diccionario()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def actualizar_factura(uuid, numero_factura, total, estado, pedido_uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "UPDATE facturas SET numero_factura=%s, total=%s, estado=%s pedido_uuid=%s WHERE uuid = %s"
        cursor.execute(sql,(numero_factura, total, estado, pedido_uuid, uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def eliminar_factura(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "DELETE FROM facturas WHERE uuid = %s"
        cursor.execute(sql,(uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def obtener_factura_por_uuid(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM facturas WHERE uuid = %s"
        cursor.execute(sql,(uuid,))
        current_app.mysql.connection.commit()
        return cursor.fetchone()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()