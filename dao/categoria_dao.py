from flask import current_app

class CategoriaDAO:

    @staticmethod
    def listar(cursor):
        sql = "SELECT * FROM categorias"
        cursor.execute(sql)
        datos = cursor.fetchall()

        return datos
    
    @staticmethod
    def insertar(cursor, uuid, nombre, descripcion):
        sql = """INSERT INTO categorias (uuid, nombre, descripcion) VALUES (%s, %s, %s)"""
        cursor.execute(sql, (uuid, nombre, descripcion))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid

        return id
    
    @staticmethod
    def actualizar(cursor, uuid, nombre, descripcion):
        sql = """UPDATE categorias SET nombre=%s, descripcion=%s WHERE uuid=%s"""
        cursor.execute(sql, (nombre, descripcion, uuid))
        current_app.mysql.connection.commit()

    @staticmethod
    def eliminar(cursor, uuid):
        sql = "DELETE FROM categorias WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def obtener_por_uuid(cursor, uuid):
        sql = "SELECT * FROM categorias WHERE uuid = %s"
        cursor.execute(sql, (uuid,))
        return cursor.fetchone() 