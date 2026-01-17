from flask import current_app
from models.pedidos_model import Pedido
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado

# Toma las filas de la base de datos utilizando inner join para 
# ref_cliente, ref_usuario, ademas del nombre del cliente donde luego se convierte en un diccionario 
def listar_pedidos():
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
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
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [Pedido(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]).ped_diccionario() for x in datos]
        return resultado
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

# Devuelve los pedidos pendientes organizados del pedido mas demorado al menos demorado
def listar_pedidos_pendientes():
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
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
            WHERE p.estado = 'pendiente'
            ORDER BY p.fecha_hora ASC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

# Genera un uuid al momento de registrar y retorna un diccionario 
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

# Utiliza uuid para acceder al pedido y retorna True o False si modifico el pedido
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

# Devuelve en forma de diccionario la fila del pedido para su uso en la validación de las demas tablas
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