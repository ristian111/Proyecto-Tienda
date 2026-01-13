from flask import current_app
from models.reportes.clientes_top_pedidos_model import ClienteTopPedidosReporte
from models.reportes.usuarios_registros_pedidos_model import UsuariosTopRegistrosPedidos

def listar_clientes_con_mas_pedidos(limit=5):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """
            SELECT
                c.nombre,
                count(*) as numero_pedidos
            FROM pedidos p 
            INNER JOIN clientes c on c.id = p.cliente_id
            GROUP BY c.id, c.nombre
            ORDER BY numero_pedidos desc
            LIMIT %s;
        """
        cursor.execute(sql, (limit,))
        datos = cursor.fetchall()
        resultados = [{"cliente": x[0], "numero_pedidos": x[1]} for x in datos]
        reporte = ClienteTopPedidosReporte(resultados).rep_diccionario()
        return reporte
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()

def listar_usuarios_con_mas_registro_pedidos(limit=5):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """
            SELECT
                u.nombre,
                count(*) as numero_pedidos
            FROM pedidos p 
            INNER JOIN usuarios u on u.id = p.usuario_id
            GROUP BY u.id, u.nombre
            ORDER BY numero_pedidos desc
            LIMIT %s;
        """
        cursor.execute(sql, (limit,))
        datos = cursor.fetchall()
        resultados = [{"usuario": x[0], "registro_pedidos": x[1]} for x in datos]
        reporte = UsuariosTopRegistrosPedidos(resultados).rep_diccionario()
        return reporte
    except Exception as e:
        current_app.mysql.connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()