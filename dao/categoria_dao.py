from flask import current_app

class CategoriaDAO:

    @staticmethod
    def listar(cursor, usuario_uuid):
        sql = "SELECT * FROM categorias WHERE usuario_uuid = %s"
        cursor.execute(sql, (usuario_uuid,))
        datos = cursor.fetchall()

        return datos
    
    @staticmethod
    def insertar(cursor, uuid, nombre, descripcion, usuario_uuid):
        sql = """INSERT INTO categorias (uuid, nombre, descripcion, usuario_uuid) VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (uuid, nombre, descripcion, usuario_uuid))
        current_app.mysql.connection.commit()
        id = cursor.lastrowid

        return id
    
    @staticmethod
    def actualizar(cursor, uuid, nombre, descripcion, usuario_uuid):
        sql = """UPDATE categorias SET nombre=%s, descripcion=%s WHERE uuid=%s AND usuario_uuid=%s"""
        cursor.execute(sql, (nombre, descripcion, uuid, usuario_uuid))
        current_app.mysql.connection.commit()

    @staticmethod
    def eliminar(cursor, uuid, usuario_uuid):
        sql = "DELETE FROM categorias WHERE uuid = %s AND usuario_uuid = %s"
        cursor.execute(sql, (uuid, usuario_uuid))
        current_app.mysql.connection.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def obtener_por_uuid(cursor, uuid, usuario_uuid):
        sql = "SELECT * FROM categorias WHERE uuid = %s AND usuario_uuid = %s"
        cursor.execute(sql, (uuid, usuario_uuid))
        return cursor.fetchone() 