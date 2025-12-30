from flask import current_app
from models.pedidos_model import Pedido
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado

def listar_pedidos():
    pedidos = current_app.mysql.connection.cursor()
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
    """
    pedidos.execute(sql)
    datos = pedidos.fetchall()
    resultado = [Pedido(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]).ped_diccionario() for x in datos]
    return resultado

def registrar_pedido(estado, total, direccion_entrega, cliente_id, usuario_id):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        uuid = str(uuidGenerado.uuid4())
        sql = "INSERT INTO pedidos (uuid, estado, total, direccion_entrega, cliente_id, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql,(uuid, estado, total, direccion_entrega, cliente_id, usuario_id))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid
        return Pedido(id, uuid, estado, total, direccion_entrega, None, None, cliente_id, usuario_id).ped_diccionario()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def actualizar_pedido(uuid, estado, total, direccion_entrega, cliente_id, usuario_id):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "UPDATE pedidos SET estado=%s, total=%s, direccion_entrega=%s, cliente_id=%s, usuario_id=%s WHERE uuid = %s"
        cursor.execute(sql,(estado, total, direccion_entrega, cliente_id, usuario_id, uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def eliminar_pedido(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "DELETE FROM pedidos WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def obtener_pedido_por_uuid(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM pedidos WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()