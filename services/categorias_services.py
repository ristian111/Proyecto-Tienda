from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from models.categorias_model import Categoria

def listar_categorias():
    categorias = current_app.mysql.connection.cursor()
    sql = "SELECT * FROM categorias"
    categorias.execute(sql)
    datos = categorias.fetchall()
    resultado = [Categoria(x[0], x[1], x[2], x[3]).cat_diccionario() for x in datos]
    return resultado

def registrar_categoria(nombre, descripcion):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        uuid = str(uuidGenerado.uuid4())
        sql = """INSERT INTO categorias (uuid, nombre, descripcion) VALUES (%s, %s, %s)"""
        cursor.execute(sql, (uuid, nombre, descripcion))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid
        return Categoria(id, uuid, nombre, descripcion).cat_diccionario()
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def actualizar_categoria(uuid, nombre, descripcion):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """UPDATE categorias SET nombre=%s, descripcion=%s WHERE uuid=%s"""
        cursor.execute(sql, (nombre, descripcion, uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def eliminar_categoria(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = "DELETE FROM categorias WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def obtener_categoria_por_uuid(uuid):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor(DictCursor)
        sql = "SELECT * FROM categorias WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone() 
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()