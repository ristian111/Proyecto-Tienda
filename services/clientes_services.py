from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models.clientes_model import Cliente

# Toma las filas de la base de datos para convertirlas en un diccionario 
def listar_clientes():
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "SELECT * FROM clientes"
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [Cliente(x[0], x[1], x[2], x[3], x[4]).cli_diccionario() for x in datos]
        return resultado
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

# Genera un uuid al momento de registrar y retorna un diccionario 
def registrar_clientes(nombre, telefono, direccion):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        uuid = str(uuidGenerado.uuid4())
        cliente = Cliente(None, None, None, telefono, None)
        sql = "INSERT INTO clientes (uuid, nombre, telefono, direccion) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (uuid, nombre, cliente.get_telefono(), direccion))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid
        return Cliente(id, uuid, nombre, telefono, direccion).cli_diccionario()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

# Utiliza uuid para acceder al cliente y retorna True o False si modifico el cliente
def actualizar_cliente(uuid, nombre, telefono, direccion):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "UPDATE clientes SET nombre=%s, telefono=%s, direccion=%s WHERE uuid=%s"
        cursor.execute(sql, (nombre, telefono, direccion, uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
       
def eliminar_cliente(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "DELETE FROM clientes WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

# Devuelve en forma de diccionario la fila del cliente para su uso en la validación de las demas tablas
def obtener_cliente_por_uuid(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM clientes WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()