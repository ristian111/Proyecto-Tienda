from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models.usuarios_model import Usuario

# Toma las filas de la base de datos para convertirlas en un diccionario 
def listar_usuarios():
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [Usuario(x[0], x[1], x[2], x[3], x[4], x[5], x[6]).usu_diccionario() for x in datos]  
        return resultado
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

# Genera un uuid al momento de registrar y retorna un diccionario
def registrar_usuario(nombre, username, password_hash, rol):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        uuid = str(uuidGenerado.uuid4())
        sql = "INSERT INTO usuarios (uuid, nombre, username, password_hash, rol) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (uuid, nombre, username, password_hash, rol))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid
        return Usuario(id, uuid, nombre, username, password_hash, rol, None).usu_diccionario()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

# Utiliza uuid para acceder a al usuario y retorna True o False si modifico al usuario
def actualizar_usuario(uuid, nombre, username, password_hash, rol):  
    cursor = None
    try:  
        cursor = current_app.mysql.connection.cursor()
        sql = "UPDATE usuarios SET nombre=%s, username=%s, password_hash=%s, rol=%s WHERE uuid=%s"
        cursor.execute(sql, (nombre, username, password_hash, rol, uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()  

def eliminar_usuario(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "DELETE FROM usuarios WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

# Devuelve en forma de diccionario la fila del usuario para su uso en la validación de las demas tablas
def obtener_usuario_por_uuid(uuid):
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM usuarios WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone()
    except Exception as e: raise e
    finally: 
        if cursor: cursor.close()

# Devuelve en forma de diccionario un registro del numero de pedidos por usuario a traves de su username
def pedidos_de_un_usuario(user):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = """
            SELECT
                u.nombre as nombre_de_usuario,
                count(p.id) as pedidos_por_usuario
            FROM usuarios u 
            LEFT JOIN pedidos p on u.id = p.usuario_id
            WHERE username = %s
            GROUP BY u.id, u.nombre
        """
        cursor.execute(sql, (user,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

# Devuelve en forma de diccionario la fila del usuario para poder autenticarlo validando su username, password_hash y rol
def obtener_usuario_por_username(user):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT uuid, username, password_hash, rol FROM usuarios WHERE username = %s"
        cursor.execute(sql, (user,))
        return cursor.fetchone()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()