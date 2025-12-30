from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models.inventarios_model import Inventario

def listar_inventarios():
    inventarios = current_app.mysql.connection.cursor()
    sql = """
        SELECT 
            i.id,
            i.uuid,
            p.uuid AS producto_uuid,
            i.cantidad_actual,
            i.cantidad_reservada,
            i.punto_reorden,
            i.ultima_actualizacion
        FROM inventarios i
        JOIN productos p ON p.id = i.producto_id
    """
    inventarios.execute(sql)
    datos = inventarios.fetchall()
    resultado = [Inventario(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).inv_diccionario() for x in datos]
    return resultado

def registrar_inventario(producto_id, cantidad_actual, cantidad_reservada, punto_reorden):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        uuid = str(uuidGenerado.uuid4())
        sql = "INSERT INTO inventarios (uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid
        return Inventario(id, uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden, None).inv_diccionario()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()


def actualizar_inventario(uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "UPDATE inventarios SET producto_id=%s, cantidad_actual=%s, cantidad_reservada=%s, punto_reorden=%s WHERE uuid=%s"
        cursor.execute(sql, (producto_id, cantidad_actual, cantidad_reservada, punto_reorden, uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def eliminar_inventario(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "DELETE FROM inventarios WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def obtener_inventario_por_uuid(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM inventarios WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()