from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models.producto_precios_model import ProductoPrecio
from .utils_db import manejar_error_base_de_datos

def registrar_precio_producto(producto_id, precio_compra, precio_venta, vigente_desde, usuario_uuid):
    try:
        uuid = str(uuidGenerado.uuid4())
        
        with current_app.mysql.connection.cursor() as cursor:
            # Cerrar el precio anterior
            sql_update = """
                UPDATE producto_precios
                SET vigente_hasta = %s, activo = 0
                WHERE producto_id = %s AND activo = 1
            """
            cursor.execute(sql_update, (vigente_desde, producto_id))

            # Insertar nuevo precio
            sql_insert = """
                INSERT INTO producto_precios (
                    uuid, producto_id, precio_compra, precio_venta, vigente_desde, vigente_hasta, activo, usuario_uuid
                ) VALUES (%s, %s, %s, %s, %s, NULL, 1, %s)
            """
            cursor.execute(sql_insert, (uuid, producto_id, precio_compra, precio_venta, vigente_desde, usuario_uuid))
            current_app.mysql.connection.commit()

            id = cursor.lastrowid
            precio = ProductoPrecio(id, uuid, producto_id, precio_compra, precio_venta, vigente_desde, None, 1)
            return precio.to_dict()

    except Exception as e:
        current_app.mysql.connection.rollback()
        manejar_error_base_de_datos(e, "producto_precios", "registrar")

def listar_precios_producto(producto_id, usuario_uuid):
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT * FROM producto_precios
            WHERE producto_id = %s AND usuario_uuid = %s
            ORDER BY vigente_desde DESC
        """
        cursor.execute(sql, (producto_id, usuario_uuid))
        return cursor.fetchall()
