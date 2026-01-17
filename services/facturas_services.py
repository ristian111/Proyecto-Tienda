from flask import current_app
import uuid as uuidGenerado
from MySQLdb.cursors import DictCursor
from models.facturas_model import Factura

# Toma las filas de la base de datos utilizando inner join para ref_pedido donde luego se convierte en un diccionario 
def listar_facturas():
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """
            SELECT
                f.id,
                f.uuid,
                f.numero_factura,
                f.total,
                f.fecha_emision,
                f.estado,
                ped.uuid
            FROM facturas f 
            INNER JOIN pedidos ped on f.pedido_id = ped.id
        """
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [Factura(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).fac_diccionario() for x in datos]
        return resultado
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

# Genera un uuid al momento de registrar y retorna un diccionario 
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

# Utiliza uuid para acceder a la factura y retorna True o False si modifico la factura
def actualizar_factura(uuid, numero_factura, total, estado, pedido_id):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "UPDATE facturas SET numero_factura=%s, total=%s, estado=%s, pedido_id=%s WHERE uuid = %s"
        cursor.execute(sql,(numero_factura, total, estado, pedido_id, uuid))
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

# Devuelve en forma de diccionario la fila de la factura para su uso en la validación de las demas tablas
def obtener_factura_por_uuid(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM facturas WHERE uuid = %s"
        cursor.execute(sql,(uuid,))
        current_app.mysql.connection.commit()
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()