from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models import Cliente
from .utils_db import manejar_error_base_de_datos

# Toma las filas de la base de datos para convertirlas en un diccionario 
def listar_clientes():
    
    with current_app.mysql.connection.cursor() as cursor:
        sql = "SELECT * FROM clientes"
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [Cliente(x[0], x[1], x[2], x[3], x[4]).cli_diccionario() for x in datos]
        return resultado

# Genera un uuid al momento de registrar y retorna un diccionario 
def registrar_clientes(nombre, telefono, direccion):
    
    try:
        uuid = str(uuidGenerado.uuid4())
        cliente = Cliente(None, uuid, nombre, telefono, direccion)
        
        with current_app.mysql.connection.cursor() as cursor:
            sql = "INSERT INTO clientes (uuid, nombre, telefono, direccion) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (uuid, nombre, cliente.get_telefono(), direccion))
            current_app.mysql.connection.commit()
            id = cursor.lastrowid
            cliente.id = id
            return cliente.cli_diccionario()
        
    except Exception as e:
        manejar_error_base_de_datos(e, "clientes", "registrar", None)
    
# Utiliza uuid para acceder al cliente y retorna True o False si modifico el cliente
def actualizar_cliente(uuid, nombre, telefono, direccion):
    
    try:
        cliente = Cliente(None, uuid, nombre, telefono, direccion)
        
        with current_app.mysql.connection.cursor() as cursor:
            sql = "UPDATE clientes SET nombre=%s, telefono=%s, direccion=%s WHERE uuid=%s"
            cursor.execute(sql, (nombre, cliente.get_telefono(), direccion, uuid))
            current_app.mysql.connection.commit()
            return cliente.cli_diccionario()
        
    except Exception as e:
        manejar_error_base_de_datos(e, "clientes", "actualizar", None)
        
def eliminar_cliente(uuid):
    
    try:
        with current_app.mysql.connection.cursor() as cursor:        
            sql = "DELETE FROM clientes WHERE uuid = %s"
            cursor.execute(sql, (uuid,))
            current_app.mysql.connection.commit()
            return cursor.rowcount > 0
    except Exception:
        current_app.mysql.connection.rollback()
        raise

# Devuelve en forma de diccionario la fila del cliente para su uso en la validación de las demas tablas
def obtener_cliente_por_uuid(uuid):
    
    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        sql = "SELECT * FROM clientes WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()
