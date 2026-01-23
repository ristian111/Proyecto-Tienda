from flask import current_app
from models.reportes.clientes import ClientesMasPedidos
from models.reportes.usuarios import UsuariosMasRegistrosPedidos
from models.reportes.productos import ProductosMasVendidos
from models.reportes.productos import ProductosMasGanancia, ProductosMasVendidos
from models.reportes.pedidos import PedidosPorFecha
from models.reportes.facturas import Ingresos

def listar_clientes_con_mas_pedidos(limit):
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
        reporte = ClientesMasPedidos(resultados).rep_diccionario()
        return reporte
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

def listar_usuarios_con_mas_registro_pedidos(limit):
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
        reporte = UsuariosMasRegistrosPedidos(resultados).rep_diccionario()
        return reporte
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

def listar_productos_mas_vendidos(desde, hasta, limit):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """
            SELECT
                prod.uuid,
                prod.nombre as producto,
                SUM(dp.cantidad) as total_vendido
            FROM productos prod
            INNER JOIN detalle_pedido dp on prod.id = dp.producto_id
            INNER JOIN pedidos ped on dp.pedido_id = ped.id
            WHERE ped.estado = 'entregado' AND
            ped.fecha_hora BETWEEN %s AND %s
            GROUP BY prod.uuid, prod.nombre
            ORDER BY total_vendido DESC
            LIMIT %s
        """
        cursor.execute(sql, (desde, hasta, limit))
        datos = cursor.fetchall()
        resultados = [{"id": x[0], "producto": x[1], "total_vendido": x[2]} for x in datos]
        reporte = ProductosMasVendidos(resultados).rep_diccionario()
        return reporte
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

def listar_pedidos_por_fecha(desde, hasta, estado=None):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """
            SELECT
                count(id) as cantidad_pedidos
            FROM pedidos 
            WHERE fecha_hora BETWEEN %s AND %s
            AND (%s IS NULL OR estado = %s)
        """
        cursor.execute(sql, (desde, hasta, estado, estado))
        datos = cursor.fetchone()
        resultados = [{"cantidad_pedidos": x} for x in datos]
        reporte = PedidosPorFecha(resultados).rep_diccionario()
        return reporte
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
 
def listar_productos_mas_ganancias(desde, hasta, limit):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """
            SELECT
                prod.uuid,
                prod.nombre as producto,
                SUM(dp.subtotal) as total_ganado
            FROM productos prod
            INNER JOIN detalle_pedido dp on prod.id = dp.producto_id
            INNER JOIN pedidos ped on dp.pedido_id = ped.id
            WHERE ped.estado = 'entregado' AND
            ped.fecha_hora BETWEEN %s AND %s
            GROUP BY prod.uuid, prod.nombre
            ORDER BY total_ganado DESC
            LIMIT %s
        """
        cursor.execute(sql, (desde, hasta, limit))
        datos = cursor.fetchall()
        resultados = [{"id": x[0], "producto": x[1], "total_ganado": x[2]} for x in datos]
        reporte = ProductosMasGanancia(resultados).rep_diccionario()
        return reporte
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()

def listar_ingresos_por_ventas(desde, hasta):
    cursor = None
    try:
        cursor = current_app.mysql.connection.cursor()
        sql = """
            SELECT
                sum(total) as ingresos
            FROM facturas 
            WHERE fecha_emision BETWEEN %s AND %s
        """
        cursor.execute(sql, (desde, hasta))
        datos = cursor.fetchone()
        resultados = [{"ingresos_generados": x} for x in datos]
        reporte = Ingresos(resultados).rep_diccionario()
        return reporte
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()