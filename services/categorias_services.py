from flask import current_app
from MySQLdb.cursors import DictCursor 
import uuid as uuidGenerado
from dao import CategoriaDAO
from models import Categoria
from .utils_db import manejar_error_base_de_datos

# Toma las filas de la base de datos para convertirlas en un diccionario 
def listar_categorias():

    with current_app.mysql.connection.cursor() as cursor:
        datos = CategoriaDAO.listar(cursor)
        resultado = [Categoria(x[0], x[1], x[2], x[3]).cat_diccionario() for x in datos]
        return resultado

# Genera un uuid al momento de registrar y retorna un diccionario
def registrar_categoria(nombre, descripcion):

    try:
        uuid = str(uuidGenerado.uuid4())
        
        with current_app.mysql.connection.cursor() as cursor:
            id = CategoriaDAO.insertar(cursor, uuid, nombre, descripcion)
            return Categoria(id, uuid, nombre, descripcion).cat_diccionario()
        
    except Exception as e:
        manejar_error_base_de_datos(e, "categoría", "registrar", "Ya existe una categoría con este nombre")
        

# Utiliza uuid para acceder a la categoria y retorna True o False si modifico la categoria
def actualizar_categoria(uuid, nombre, descripcion):

    try:
        with current_app.mysql.connection.cursor() as cursor:
            CategoriaDAO.actualizar(cursor, uuid, nombre, descripcion)
            return Categoria(None, uuid, nombre, descripcion).cat_diccionario()
        
    except Exception as e:
        manejar_error_base_de_datos(e, "categoría", "actualizar", "Ya existe una categoría con este nombre")

def eliminar_categoria(uuid):

    try:
        with current_app.mysql.connection.cursor() as cursor:
            resultado = CategoriaDAO.eliminar(cursor, uuid)
            return resultado
    except Exception:
        current_app.mysql.connection.rollback()
        raise

# Devuelve en forma de diccionario la fila de la categoria para su uso en la validación de las demas tablas
def obtener_categoria_por_uuid(uuid):

    with current_app.mysql.connection.cursor(DictCursor) as cursor:
        resultado = CategoriaDAO.obtener_por_uuid(cursor, uuid)
        return resultado
