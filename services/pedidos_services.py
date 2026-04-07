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
                cli.nombre as nombre_cliente,
                cli.uuid as referencia_cliente,
                u.uuid as referencia_usuario
            FROM pedidos pe INNER JOIN clientes cli on pe.cliente_id = cli.id
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
                c.nombre as nombre_cliente,
                p.estado as estado_pedido,
                p.direccion_entrega,
                p.fecha_hora as hora_pedido,
                p.total
            FROM pedidos p
            INNER JOIN clientes c on p.cliente_id = c.id
            WHERE p.estado = 'pendiente' AND p.usuario_uuid = %s
            ORDER BY p.fecha_hora ASC
        """
        cursor.execute(sql, (usuario_uuid,))
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