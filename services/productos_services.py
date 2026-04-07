from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models import Producto
from .utils_db import manejar_error_base_de_datos

# Toma las filas de la base de datos utilizando inner join para ref_categoria donde luego se convierte en un diccionario 
def listar_productos(usuario_uuid):
    
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT 
                p.uuid as ref,
                p.nombre,
                p.precio_venta,
                p.costo_promedio,
                p.unidad_medida,
                c.uuid AS ref_categoria
            FROM productos p
            JOIN categorias c ON c.id = p.categoria_id
            WHERE p.usuario_uuid = %s
        """
        cursor.execute(sql, (usuario_uuid,))
        return cursor.fetchall()

# Genera un uuid al momento de registrar y retorna un diccionario 
def registrar_producto(nombre, precio_venta, costo_promedio, unidad_medida, categoria_id, categoria_uuid, usuario_uuid):
    
    try:
        uuid = str(uuidGenerado.uuid4())
        producto = Producto(None, uuid, nombre, precio_venta, costo_promedio, unidad_medida, categoria_uuid)
        
        with current_app.mysql.connection.cursor() as cursor:
            
            sql = """INSERT INTO productos (
            uuid, nombre, precio_venta, costo_promedio, unidad_medida, categoria_id, usuario_uuid
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (uuid, nombre, producto.get_precio_venta(), producto.get_costo_promedio(), unidad_medida, categoria_id, usuario_uuid))
            current_app.mysql.connection.commit()
            id = cursor.lastrowid
            producto.id = id
            return producto.prod_diccionario()
        
    except Exception as e:
        current_app.mysql.connection.rollback()
        manejar_error_base_de_datos(e, "producto", "registrar")

# Utiliza uuid para acceder al producto y retorna True o False si modifico el producto
def actualizar_producto(uuid, nombre, precio_venta, costo_promedio, unidad_medida, categoria_id, categoria_uuid, usuario_uuid):
    
    try:
        producto = Producto(None, uuid, nombre, precio_venta, costo_promedio, unidad_medida, categoria_uuid)
        
        with current_app.mysql.connection.cursor() as cursor:

            sql = """UPDATE productos SET 
            nombre=%s, precio_venta=%s, costo_promedio=%s, unidad_medida=%s, categoria_id=%s
            WHERE uuid=%s AND usuario_uuid=%s
            """
            cursor.execute(sql, (nombre, producto.get_precio_venta(), producto.get_costo_promedio(), unidad_medida, categoria_id, uuid, usuario_uuid))
            current_app.mysql.connection.commit()
            return producto.prod_diccionario()
        
    except Exception as e:
         current_app.mysql.connection.rollback()
         manejar_error_base_de_datos(e, "producto", "actualizar")

def eliminar_producto(uuid, usuario_uuid):
    
    try:
        with current_app.mysql.connection.cursor() as cursor:
            sql = "DELETE FROM productos WHERE uuid = %s AND usuario_uuid = %s"
            cursor.execute(sql, (uuid, usuario_uuid))
            current_app.mysql.connection.commit()
            return cursor.rowcount > 0
    except Exception:
        current_app.mysql.connection.rollback()
        raise 

# Devuelve en forma de diccionario la fila del producto para su uso en la validación de las demas tablas
def obtener_producto_por_uuid(uuid, usuario_uuid):
    
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = "SELECT * FROM productos WHERE uuid = %s AND usuario_uuid = %s"
        cursor.execute(sql, (uuid, usuario_uuid))
        return cursor.fetchone()