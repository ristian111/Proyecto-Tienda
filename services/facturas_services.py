import uuid as uuidGenerado
from flask import current_app
from datetime import datetime
from MySQLdb.cursors import DictCursor
from models import Factura

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
def registrar_factura(pedido_id, venta_presencial, pedido_uuid):
    cursor = None
    conn = current_app.mysql.connection

    try:
        cursor = conn.cursor(DictCursor)
        conn.begin()

        #Calcular total de detalle_pedido
        sql_pedido = "SELECT SUM(subtotal) as total FROM detalle_pedido WHERE pedido_id = %s"
        cursor.execute(sql_pedido, (pedido_id,))
        datos = cursor.fetchone()

        if not datos or datos["total"] is None:
            raise ValueError("El pedido no tiene detalle")
        
        total = datos["total"]

        #Actualizar total del pedido
        sql_actualizar_pedido = "UPDATE pedidos SET total = %s WHERE id = %s"
        cursor.execute(sql_actualizar_pedido, (total, pedido_id))

        #Validar stock
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
            raise ValueError("Stock insuficiente")
        
        #Insertar factura
        factura_uuid = str(uuidGenerado.uuid4())
        numero_factura = f"FAC-{datetime.now().strftime('%Y%m%d')}-{factura_uuid[:8]}"
        estado = "pagada" if venta_presencial else "emitida"

        sql_insertar_factura = """
            INSERT INTO facturas (uuid, numero_factura, total, estado, pedido_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insertar_factura, (factura_uuid, numero_factura, total, estado, pedido_id))
        id = cursor.lastrowid
        
        #Actualizar inventario
        sql_actualizar_inventario = """
            UPDATE inventarios i INNER JOIN productos p on i.producto_id = p.id 
            INNER JOIN detalle_pedido dp on p.id = dp.producto_id

            SET i.cantidad_actual = i.cantidad_actual - dp.cantidad
            WHERE dp.pedido_id = %s
        """
        cursor.execute(sql_actualizar_inventario, (pedido_id,))

        #Actualizar estado del pedido
        sql_actualizar_estado_pedido = "UPDATE pedidos SET estado = %s WHERE id = %s"
        cursor.execute(sql_actualizar_estado_pedido, ("entregado" if not venta_presencial else "pendiente", pedido_id))

        conn.commit()

        sql_factura = "SELECT fecha_emision FROM facturas WHERE id = %s"
        cursor.execute(sql_factura, (id,))
        dato = cursor.fetchone()
        fecha_emision = dato["fecha_emision"]
        resultado = Factura(id, factura_uuid, numero_factura, total, fecha_emision, estado, pedido_uuid).fac_diccionario()
        return resultado
    
    except Exception as e:
        conn.rollback()
        if isinstance(e, ValueError):
            raise e 
        raise e
    finally:
        if cursor:
            cursor.close()

# Utiliza uuid para acceder a la factura y retorna True o False si modifico la factura
def actualizar_factura(uuid, numero_factura, total, estado, pedido_id, pedido_uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        factura = Factura(None, None, numero_factura, total, datetime.now(), estado, pedido_uuid)
        sql = "UPDATE facturas SET numero_factura=%s, total=%s, estado=%s, pedido_id=%s WHERE uuid = %s"
        cursor.execute(sql,(numero_factura, total, estado, pedido_id, uuid))
        current_app.mysql.connection.commit()
        return factura.fac_diccionario()
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