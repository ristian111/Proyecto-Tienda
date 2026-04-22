import uuid as uuidGenerado
from flask import current_app
from datetime import datetime
from MySQLdb.cursors import DictCursor
from models import Factura
from .utils_db import manejar_error_base_de_datos
from utils import errores

def listar_facturas(usuario_uuid, fecha_inicio=None, fecha_fin=None):
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT
                f.uuid as ref,
                f.numero_factura,
                f.total,
                f.fecha_emision,
                f.estado,
                ped.uuid as ref_pedido,
                dp.cantidad as producto_cantidad,
                dp.precio_unitario as producto_precio_unitario,
                dp.subtotal as producto_subtotal,
                p.nombre as producto_nombre
            FROM facturas f 
            INNER JOIN pedidos ped on f.pedido_id = ped.id
            INNER JOIN detalle_pedido dp on f.pedido_id = dp.pedido_id
            INNER JOIN productos p on dp.producto_id = p.id
            WHERE f.usuario_uuid = %s
        """
        params = [usuario_uuid]
        
        if fecha_inicio and fecha_inicio.strip():
            sql += " AND f.fecha_emision >= %s"
            params.append(f"{fecha_inicio.strip()} 00:00:00")
            
        if fecha_fin and fecha_fin.strip():
            sql += " AND f.fecha_emision <= %s"
            params.append(f"{fecha_fin.strip()} 23:59:59")
        
        sql += " ORDER BY f.fecha_emision DESC"
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        facturas_dict = {}
        for row in rows:
            f_ref = row['ref']
            if f_ref not in facturas_dict:
                facturas_dict[f_ref] = {
                    "ref": f_ref,
                    "numero_factura": row['numero_factura'],
                    "total": row['total'],
                    "fecha_emision": row['fecha_emision'],
                    "estado": row['estado'],
                    "ref_pedido": row['ref_pedido'],
                    "cantidad_productos": 0,
                    "detalles": []
                }
            
            facturas_dict[f_ref]["cantidad_productos"] += int(row['producto_cantidad'])
            facturas_dict[f_ref]["detalles"].append({
                "nombre": row['producto_nombre'],
                "cantidad": row['producto_cantidad'],
                "precio_unitario": row['producto_precio_unitario'],
                "subtotal": row['producto_subtotal']
            })
            
        return list(facturas_dict.values())
    
def registrar_factura(pedido_id, venta_presencial, pedido_uuid, usuario_uuid):
    conn = current_app.mysql.connection

    try:
        with conn.cursor(DictCursor) as cursor:
            conn.begin()

            sql_pedido = "SELECT SUM(subtotal) as total FROM detalle_pedido WHERE pedido_id = %s"
            cursor.execute(sql_pedido, (pedido_id,))
            datos = cursor.fetchone()

            if not datos or datos["total"] is None:
                raise errores.ErrorNegocio("El pedido no tiene detalle")

            total = datos["total"]

            sql_actualizar_pedido = "UPDATE pedidos SET total = %s WHERE id = %s"
            cursor.execute(sql_actualizar_pedido, (total, pedido_id))

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

            factura_uuid = str(uuidGenerado.uuid4())
            numero_factura = f"FAC-{datetime.now().strftime('%Y%m%d')}-{factura_uuid[:8]}"
            estado = "pagada" if venta_presencial else "emitida"

            sql_insertar_factura = """
                INSERT INTO facturas (uuid, numero_factura, total, estado, pedido_id, usuario_uuid)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insertar_factura, (factura_uuid, numero_factura, total, estado, pedido_id, usuario_uuid))
            factura_id = cursor.lastrowid

            sql_actualizar_inventario = """
                UPDATE inventarios i INNER JOIN productos p on i.producto_id = p.id 
                INNER JOIN detalle_pedido dp on p.id = dp.producto_id

                SET i.cantidad_actual = i.cantidad_actual - dp.cantidad
                WHERE dp.pedido_id = %s
            """
            cursor.execute(sql_actualizar_inventario, (pedido_id,))

            sql_actualizar_estado_pedido = "UPDATE pedidos SET estado = %s WHERE id = %s"
            cursor.execute(sql_actualizar_estado_pedido, ("entregado" if venta_presencial else "pendiente", pedido_id))

            conn.commit()

            fecha_emision = datetime.now()
            resultado = Factura(factura_id, factura_uuid, numero_factura, total, fecha_emision, estado, pedido_uuid).fac_diccionario()
            return resultado
    
    except Exception as e:
        conn.rollback()
        manejar_error_base_de_datos(e, "factura", "registrar", "No puede haber dos facturas para este pedido")

def actualizar_factura(uuid, numero_factura, total, estado, pedido_id, pedido_uuid, usuario_uuid):
    try:
        factura = Factura(None, uuid, numero_factura, total, datetime.now().isoformat(), estado, pedido_uuid)
        
        with current_app.mysql.connection.cursor() as cursor:
            sql = "UPDATE facturas SET numero_factura=%s, total=%s, estado=%s, pedido_id=%s WHERE uuid = %s AND usuario_uuid = %s"
            cursor.execute(sql,(numero_factura, total, estado, pedido_id, uuid, usuario_uuid))
            current_app.mysql.connection.commit()
            return factura.fac_diccionario()
        
    except Exception as e:
        current_app.mysql.connection.rollback()
        manejar_error_base_de_datos(e, "factura", "registrar", "No puede haber dos facturas para este pedido") 

def eliminar_factura(uuid, usuario_uuid):
    try:
        with current_app.mysql.connection.cursor() as cursor:
            sql = "DELETE FROM facturas WHERE uuid = %s AND usuario_uuid = %s"
            cursor.execute(sql,(uuid, usuario_uuid))
            current_app.mysql.connection.commit()
            return cursor.rowcount > 0
        
    except Exception:
        current_app.mysql.connection.rollback()
        raise 

def obtener_factura_por_uuid(uuid, usuario_uuid):
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = "SELECT * FROM facturas WHERE uuid = %s AND usuario_uuid = %s"
        cursor.execute(sql,(uuid, usuario_uuid))
        return cursor.fetchone()