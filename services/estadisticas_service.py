from flask import current_app
from MySQLdb.cursors import DictCursor

def resumen_hoy(usuario_uuid):
    conn = current_app.mysql.connection
    cursor = conn.cursor(DictCursor)
    try:
        cursor.execute("""
            SELECT 
                COUNT(p.id) as num_ventas,
                COALESCE(SUM(p.total), 0) as ventas_hoy
            FROM pedidos p
            WHERE p.usuario_uuid = %s 
              AND DATE(p.fecha_hora) = CURDATE()
        """, (usuario_uuid,))
        res_pedidos = cursor.fetchone()
        
        num_ventas = res_pedidos['num_ventas'] if res_pedidos else 0
        ventas_hoy = float(res_pedidos['ventas_hoy']) if res_pedidos and res_pedidos['ventas_hoy'] else 0.0
        
        cursor.execute("""
            SELECT 
                COALESCE(SUM(dp.subtotal - (dp.cantidad * pr.costo_promedio)), 0) as ganancia_hoy
            FROM detalle_pedido dp
            JOIN pedidos p ON dp.pedido_id = p.id
            JOIN productos pr ON dp.producto_id = pr.id
            WHERE p.usuario_uuid = %s 
              AND DATE(p.fecha_hora) = CURDATE()
        """, (usuario_uuid,))
        res_ganancia = cursor.fetchone()
        ganancia_hoy = float(res_ganancia['ganancia_hoy']) if res_ganancia and res_ganancia['ganancia_hoy'] is not None else 0.0

        ticket_promedio = (ventas_hoy / num_ventas) if num_ventas > 0 else 0

        return {
            "ventas_hoy": ventas_hoy,
            "ganancia_hoy": ganancia_hoy,
            "ticket_promedio": ticket_promedio
        }
    finally:
        cursor.close()

def top_productos(usuario_uuid, filtro_tiempo="mensual"):
    conn = current_app.mysql.connection
    cursor = conn.cursor(DictCursor)
    try:
        where_clause = "p.usuario_uuid = %s"
        if filtro_tiempo == "diario":
            where_clause += " AND DATE(p.fecha_hora) = CURDATE()"
        elif filtro_tiempo == "semanal":
            where_clause += " AND YEARWEEK(p.fecha_hora, 1) = YEARWEEK(CURDATE(), 1)"
        else:
            where_clause += " AND MONTH(p.fecha_hora) = MONTH(CURDATE()) AND YEAR(p.fecha_hora) = YEAR(CURDATE())"

        query = f"""
            SELECT pr.nombre, SUM(dp.cantidad) as cantidad_vendida
            FROM detalle_pedido dp
            JOIN pedidos p ON dp.pedido_id = p.id
            JOIN productos pr ON dp.producto_id = pr.id
            WHERE {where_clause}
            GROUP BY pr.id
            ORDER BY cantidad_vendida DESC
            LIMIT 5
        """
        cursor.execute(query, (usuario_uuid,))
        resultados = cursor.fetchall()
        return [{"nombre": r["nombre"], "cantidad": int(r["cantidad_vendida"])} for r in resultados]
    finally:
        cursor.close()

def ingresos_ganancias(usuario_uuid, dias=7):
    conn = current_app.mysql.connection
    cursor = conn.cursor(DictCursor)
    try:
        query = """
            SELECT 
                DATE(p.fecha_hora) as fecha,
                COALESCE(SUM(dp.subtotal), 0) as ingreso,
                COALESCE(SUM(dp.subtotal - (dp.cantidad * pr.costo_promedio)), 0) as ganancia
            FROM pedidos p
            JOIN detalle_pedido dp ON p.id = dp.pedido_id
            JOIN productos pr ON dp.producto_id = pr.id
            WHERE p.usuario_uuid = %s 
              AND p.fecha_hora >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            GROUP BY DATE(p.fecha_hora)
            ORDER BY fecha ASC
        """
        cursor.execute(query, (usuario_uuid, dias))
        resultados = cursor.fetchall()
        
        return [{
            "fecha": r["fecha"].strftime("%Y-%m-%d"),
            "ingreso": float(r["ingreso"]),
            "ganancia": float(r["ganancia"])
        } for r in resultados]
    finally:
        cursor.close()

def productos_estancados(usuario_uuid):
    conn = current_app.mysql.connection
    cursor = conn.cursor(DictCursor)
    try:
        query = """
            SELECT 
                pr.nombre, 
                pr.uuid as ref,
                COALESCE(inv.cantidad_actual, 0) as stock,
                (
                    SELECT DATEDIFF(CURDATE(), MAX(p.fecha_hora))
                    FROM detalle_pedido dp2
                    JOIN pedidos p ON dp2.pedido_id = p.id
                    WHERE dp2.producto_id = pr.id
                ) as dias_estancado
            FROM productos pr
            LEFT JOIN inventarios inv ON pr.id = inv.producto_id
            WHERE pr.usuario_uuid = %s AND pr.id NOT IN (
                SELECT DISTINCT dp.producto_id 
                FROM detalle_pedido dp
                JOIN pedidos p ON dp.pedido_id = p.id
                WHERE p.usuario_uuid = %s AND p.fecha_hora >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            )
        """
        cursor.execute(query, (usuario_uuid, usuario_uuid))
        resultados = cursor.fetchall()
        
        return [{
            "nombre": r["nombre"], 
            "ref": r["ref"],
            "stock": int(r["stock"]),
            "dias_estancado": r["dias_estancado"] if r["dias_estancado"] is not None else "Nunca"
        } for r in resultados]
    finally:
        cursor.close()

def porcentaje_categorias(usuario_uuid):
    conn = current_app.mysql.connection
    cursor = conn.cursor(DictCursor)
    try:
        query = """
            SELECT c.nombre, COUNT(dp.id) as total_vendidos
            FROM detalle_pedido dp
            JOIN pedidos p ON dp.pedido_id = p.id
            JOIN productos pr ON dp.producto_id = pr.id
            JOIN categorias c ON pr.categoria_id = c.id
            WHERE p.usuario_uuid = %s AND DATE(p.fecha_hora) >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY c.id
        """
        cursor.execute(query, (usuario_uuid,))
        resultados = cursor.fetchall()
        return [{"nombre": r["nombre"], "vendidos": r["total_vendidos"]} for r in resultados]
    finally:
        cursor.close()