from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models import Producto
from .utils_db import manejar_error_base_de_datos

# Toma las filas de la base de datos utilizando inner join para ref_categoria donde luego se convierte en un diccionario 
def listar_productos():
    
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT 
                p.uuid as ref,
                p.nombre,
                p.precio_venta,
                p.precio_compra,
                p.unidad_medida,
                c.uuid AS ref_categoria
            FROM productos p
            JOIN categorias c ON c.id = p.categoria_id
        """
        cursor.execute(sql)
        return cursor.fetchall()

# Genera un uuid al momento de registrar y retorna un diccionario 
def registrar_producto(nombre, precio_venta, precio_compra, unidad_medida, categoria_id, categoria_uuid):
    
    try:
        uuid = str(uuidGenerado.uuid4())
        producto = Producto(None, uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_uuid)
        
        with current_app.mysql.connection.cursor() as cursor:
            
            sql = """INSERT INTO productos (
            uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_id
            ) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (uuid, nombre, producto.get_precio_venta(), producto.get_precio_compra(), unidad_medida, categoria_id))
            current_app.mysql.connection.commit()
            id = cursor.lastrowid
            producto.id = id
            return producto.prod_diccionario()
        
    except Exception as e:
        current_app.mysql.connection.rollback()
        manejar_error_base_de_datos(e, "producto", "registrar")

# Utiliza uuid para acceder al producto y retorna True o False si modifico el producto
def actualizar_producto(uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_id, categoria_uuid):
    
    try:
        producto = Producto(None, uuid, nombre, precio_venta, precio_compra, unidad_medida, categoria_uuid)
        
        with current_app.mysql.connection.cursor() as cursor:

            sql = """UPDATE productos SET 
            nombre=%s, precio_venta=%s, precio_compra=%s, unidad_medida=%s, categoria_id=%s
            WHERE uuid=%s
            """
            cursor.execute(sql, (nombre, producto.get_precio_venta(), producto.get_precio_compra(), unidad_medida, categoria_id, uuid))
            current_app.mysql.connection.commit()
            return producto.prod_diccionario()
        
    except Exception as e:
         current_app.mysql.connection.rollback()
         manejar_error_base_de_datos(e, "producto", "actualizar")

def eliminar_producto(uuid):
    
    try:
        with current_app.mysql.connection.cursor() as cursor:
            sql = "DELETE FROM productos WHERE uuid = %s"
            cursor.execute(sql, (uuid,))
            current_app.mysql.connection.commit()
            return cursor.rowcount > 0
    except Exception:
        current_app.mysql.connection.rollback()
        raise 

# Devuelve en forma de diccionario la fila del producto para su uso en la validación de las demas tablas
def obtener_producto_por_uuid(uuid):
    
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = "SELECT * FROM productos WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()