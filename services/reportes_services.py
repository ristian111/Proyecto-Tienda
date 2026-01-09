from flask import current_app
from models.reportes_models import ClientePedidosReporte

def listar_clientes_con_mas_pedidos():
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
            LIMIT 5;
        """
        cursor.execute(sql)
        datos = cursor.fetchall()
        resultado = [ClientePedidosReporte(x[0], x[1]).clientes_con_mas_pedidos() for x in datos]
        return resultado
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()