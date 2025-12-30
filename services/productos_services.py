from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models.productos_models import Producto

def listar_productos():
    productos = current_app.mysql.connection.cursor()
    sql = """
        SELECT 
            p.id,
            p.uuid,
            p.nombre,
            p.precio_venta,
            p.precio_compra,
            p.unidad_medida,
            c.uuid AS categoria_uuid
        FROM productos p
        JOIN categorias c ON c.id = p.categoria_id
    """
    productos.execute(sql)
    datos = productos.fetchall()
    resultado = [Producto(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).prod_diccionario() for x in datos]
    return resultado

def registrar_producto(nombre, precio_venta, precio_compra, unidad_medida, categoria_id):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        uuid = str(uuidGenerado.uuid4())
        sql = """INSERT INTO productos (
        uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_id
        ) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_id))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid
        return Producto(id, uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_id).prod_diccionario()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def actualizar_producto(uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_id):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """UPDATE productos SET 
        nombre=%s, precio_venta=%s, precio_compra=%s, unidad_medida=%s, categoria_id=%s
        WHERE uuid=%s
        """
        cursor.execute(sql, (nombre, precio_venta, precio_compra, unidad_medida, categoria_id, uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def eliminar_producto(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "DELETE FROM productos WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def obtener_producto_por_uuid(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM productos WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()