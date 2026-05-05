from flask import current_app
from models import Pedido
from datetime import datetime
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from .utils_db import manejar_error_base_de_datos

# Toma las filas de la base de datos utilizando inner join para 
# ref_cliente, ref_usuario, ademas del nombre del cliente donde luego se convierte en un diccionario 
def listar_pedidos(usuario_uuid):

    with current_app.mysql.connection.cursor() as cursor:
        sql = """
            SELECT
                pe.id,
                pe.uuid,
                pe.estado, 
                pe.total,
                pe.direccion_entrega,
                pe.fecha_hora,
                COALESCE(cli.nombre, 'Venta Mostrador') as nombre_cliente,
                cli.uuid as referencia_cliente,
                u.uuid as referencia_usuario
            FROM pedidos pe 
            LEFT JOIN clientes cli on pe.cliente_id = cli.id
            INNER JOIN usuarios u on pe.usuario_id = u.id
            WHERE pe.usuario_uuid = %s
            ORDER BY pe.id desc
        """
        cursor.execute(sql, (usuario_uuid,))
        datos = cursor.fetchall()
        resultado = [Pedido(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]).ped_diccionario() for x in datos]
        return resultado

# Devuelve los pedidos pendientes organizados del pedido mas demorado al menos demorado
def listar_pedidos_pendientes(usuario_uuid):

    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT
                p.uuid as id_pedido,
                COALESCE(c.nombre, 'Venta Mostrador') as nombre_cliente,
                p.estado as estado_pedido,
                p.direccion_entrega,
                p.fecha_hora as hora_pedido,
                p.total
            FROM pedidos p
            LEFT JOIN clientes c on p.cliente_id = c.id
            WHERE p.estado = 'pendiente' AND p.usuario_uuid = %s
            ORDER BY p.fecha_hora ASC
        """
        cursor.execute(sql, (usuario_uuid,))
        return cursor.fetchall()

def listar_detalles_pedido(pedido_uuid):
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = """
            SELECT 
                dp.cantidad, 
                dp.subtotal as subtotal, 
                (dp.subtotal / dp.cantidad) as precio_unitario,
                p.nombre as producto_nombre 
            FROM detalle_pedido dp 
            INNER JOIN pedidos pe ON dp.pedido_id = pe.id 
            INNER JOIN productos p ON dp.producto_id = p.id 
            WHERE pe.uuid = %s
        """
        cursor.execute(sql, (pedido_uuid,))
        return cursor.fetchall()

# Genera un uuid al momento de registrar y retorna un diccionario 
def registrar_pedido(estado, total, direccion_entrega, cliente_id, usuario_id, cliente_uuid, usuario_uuid):
    
    try:
        uuid = str(uuidGenerado.uuid4())
        print("hola")
        with current_app.mysql.connection.cursor(DictCursor) as cursor:
            sql = "INSERT INTO pedidos (uuid, estado, total, direccion_entrega, cliente_id, usuario_id, usuario_uuid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(uuid, estado, total, direccion_entrega, cliente_id, usuario_id, usuario_uuid))
            current_app.mysql.connection.commit()
            id = cursor.lastrowid
            sql_cliente = "SELECT nombre FROM clientes WHERE uuid = %s"
            cursor.execute(sql_cliente, (cliente_uuid,))
            dato = cursor.fetchone()
            nombre_cliente = dato["nombre"]
            return Pedido(id, uuid, estado, total, direccion_entrega, datetime.now().isoformat(), nombre_cliente, cliente_uuid, usuario_uuid).ped_diccionario()
        
    except Exception as e:
        manejar_error_base_de_datos(e, "pedido", "registrar")
        
# Utiliza uuid para acceder al pedido y retorna True o False si modifico el pedido
def actualizar_pedido(uuid, estado, total, direccion_entrega, cliente_id, usuario_id, cliente_uuid, usuario_uuid):
    
    try:
        with current_app.mysql.connection.cursor(DictCursor) as cursor:
            sql = "UPDATE pedidos SET estado=%s, total=%s, direccion_entrega=%s, cliente_id=%s, usuario_id=%s WHERE uuid = %s AND usuario_uuid = %s"
            cursor.execute(sql,(estado, total, direccion_entrega, cliente_id, usuario_id, uuid, usuario_uuid))
            current_app.mysql.connection.commit()
            sql_cliente = "SELECT nombre FROM clientes WHERE uuid = %s"
            cursor.execute(sql_cliente, (cliente_uuid,))
            dato = cursor.fetchone()
            nombre_cliente = dato["nombre"]
            return Pedido(None, uuid, estado, total, direccion_entrega, datetime.now().isoformat(), nombre_cliente, cliente_uuid, usuario_uuid).ped_diccionario()
    except Exception as e:
        manejar_error_base_de_datos(e, "pedido", "actualizar")

def eliminar_pedido(uuid, usuario_uuid):
    
    try:
        with current_app.mysql.connection.cursor() as cursor:
            sql = "DELETE FROM pedidos WHERE uuid = %s AND usuario_uuid = %s"
            cursor.execute(sql, (uuid, usuario_uuid))
            current_app.mysql.connection.commit()
            return cursor.rowcount > 0
    except Exception:
        current_app.mysql.connection.rollback()
        raise
    
# Devuelve en forma de diccionario la fila del pedido para su uso en la validación de las demas tablas
def obtener_pedido_por_uuid(uuid, usuario_uuid):
    
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = "SELECT * FROM pedidos WHERE uuid = %s AND usuario_uuid = %s"
        cursor.execute(sql, (uuid, usuario_uuid))
        return cursor.fetchone()

def registrar_pedido_rapido(items, usuario_uuid, fecha_manual=None):
    if fecha_manual:
        try:
            if 'T' in fecha_manual:
                fecha_obj = datetime.fromisoformat(fecha_manual)
            else:
                fecha_obj = datetime.strptime(fecha_manual, '%Y-%m-%d %H:%M:%S')
        except Exception:
            fecha_obj = datetime.now()
    else:
        fecha_obj = datetime.now()

    conn = current_app.mysql.connection
    cursor = conn.cursor(DictCursor)

    try:
        total = sum(item['cantidad'] * item['precio_unitario'] for item in items)

        cursor.execute("SELECT id FROM usuarios WHERE uuid = %s", (usuario_uuid,))
        usuario = cursor.fetchone()
        if not usuario:
            raise ValueError("Usuario no encontrado")
        usuario_id = usuario['id']

        pedido_uuid = str(uuidGenerado.uuid4())
        cursor.execute(
            """INSERT INTO pedidos (uuid, estado, total, usuario_id, usuario_uuid, fecha_hora)
               VALUES (%s, 'pendiente', %s, %s, %s, %s)""",
            (pedido_uuid, total, usuario_id, usuario_uuid, fecha_obj)
        )
        pedido_id = cursor.lastrowid

        for item in items:
            ref_producto = item['ref_producto']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']
            subtotal = cantidad * precio_unitario

            cursor.execute(
                "SELECT id FROM productos WHERE uuid = %s AND usuario_uuid = %s",
                (ref_producto, usuario_uuid)
            )
            producto = cursor.fetchone()
            if not producto:
                raise ValueError(f"Producto {ref_producto} no encontrado")
            producto_id = producto['id']

            cursor.execute(
                """INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario, subtotal, usuario_uuid)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (pedido_id, producto_id, cantidad, precio_unitario, subtotal, usuario_uuid)
            )

        conn.commit()

        return {
            "ref": pedido_uuid,
            "total": total,
            "items": len(items),
            "fecha": fecha_obj.isoformat(),
            "estado": "pendiente"
        }

    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()