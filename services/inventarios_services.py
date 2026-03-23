from flask import current_app, request
from datetime import datetime
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models import Inventario, MovimientoInventario
from .utils_db import manejar_error_base_de_datos

# Toma las filas de la base de datos utilizando inner join para ref_producto donde luego se convierte en un diccionario 
def listar_inventarios():

    with current_app.mysql.connection.cursor() as cursor:
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
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [Inventario(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).inv_diccionario() for x in datos]
        return resultado

# Genera un uuid al momento de registrar y retorna un diccionario 
def registrar_inventario(producto_id, cantidad_actual, cantidad_reservada, punto_reorden):
    
    usuario_id = request.usuario["uuid"]
    cursor.execute("SET @usuario_app = %s", (usuario_id,))
    
    try:
        uuid = str(uuidGenerado.uuid4())
        inventario = Inventario(None, uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden, datetime.now().isoformat())
        
        with current_app.mysql.connection.cursor() as cursor:
            sql = "INSERT INTO inventarios (uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (uuid, producto_id, inventario.get_cantidad_actual(), inventario.get_cantidad_reservada(), inventario.get_punto_reorden()))
            current_app.mysql.connection.commit()
            id = cursor.lastrowid
            inventario.id = id
            return inventario.inv_diccionario()
        
    except Exception as e:
        manejar_error_base_de_datos(e, "inventario", "registrar", "Ya existe un inventario para este producto")

# Utiliza uuid para acceder al inventario y retorna True o False si modifico el inventario
def actualizar_inventario(uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden, producto_uuid):
    
    usuario_id = request.usuario["uuid"]
    cursor.execute("SET @usuario_app = %s", (usuario_id,))
    
    try:
        inventario = Inventario(None, uuid, producto_uuid, cantidad_actual, cantidad_reservada, punto_reorden, datetime.now().isoformat())
        
        with current_app.mysql.connection.cursor() as cursor:
            sql = "UPDATE inventarios SET producto_id=%s, cantidad_actual=%s, cantidad_reservada=%s, punto_reorden=%s WHERE uuid=%s"
            cursor.execute(sql, (producto_id, inventario.get_cantidad_actual(), inventario.get_cantidad_reservada, inventario.get_punto_reorden(), uuid))
            current_app.mysql.connection.commit()
            return inventario.inv_diccionario()
        
    except Exception as e:
        manejar_error_base_de_datos(e, "inventario", "actualizar", "Ya existe un inventario para este producto")

def eliminar_inventario(uuid):
    
    usuario_id = request.usuario["uuid"]
    cursor.execute("SET @usuario_app = %s", (usuario_id,))
    
    try:
        with current_app.mysql.connection.cursor() as cursor:
            sql = "DELETE FROM inventarios WHERE uuid = %s"
            cursor.execute(sql, (uuid,))
            current_app.mysql.connection.commit()
            return cursor.rowcount > 0
    except Exception:
        current_app.mysql.connection.rollback()
        raise 

# Devuelve en forma de diccionario el producto o productos con stock mas bajos
def listar_productos_stock_bajo(limit):
    
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT
                prod.nombre as producto,
                i.cantidad_actual as inventario_actual,
                i.cantidad_reservada,
                i.punto_reorden
            FROM inventarios i 
            INNER JOIN productos prod on prod.id = i.producto_id
            WHERE i.cantidad_actual <= punto_reorden + 2
            LIMIT %s
        """
        cursor.execute(sql, (limit,))
        return cursor.fetchall(limit)


# Devuelve stock del producto buscado
def listar_stock_producto(producto):
    
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT
                prod.nombre as producto,
                i.cantidad_actual as inventario_actual,
                i.cantidad_reservada,
                i.punto_reorden,
                i.ultima_actualizacion as ultima_modificacion
            FROM inventarios i 
            INNER JOIN productos prod on prod.id = i.producto_id
            WHERE prod.nombre = %s
        """
        cursor.execute(sql, (producto,))
        return cursor.fetchone()

def listar_movimiento_inventario():
    
    with current_app.mysql.connection.cursor() as cursor:
        sql = "SELECT * FROM movimiento_inventario"
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [MovimientoInventario(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], 
                                          x[8], x[9], x[10], x[11]).mov_inv_diccionario() for x in datos]
        return resultado

# Devuelve en forma de diccionario la fila del inventario para su uso en la validación de las demas tablas
def obtener_inventario_por_uuid(uuid):

    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = "SELECT * FROM inventarios WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()
