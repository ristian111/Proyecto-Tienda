from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from datetime import datetime


def registrar_venta_rapida(items, usuario_uuid, fecha_manual=None):
    """
    Transacción atómica: crea pedido + detalles + descuenta inventario.
    items = [{ ref_producto, cantidad, precio_unitario }, ...]
    """
    # Determinar la fecha a usar
    if fecha_manual:
        try:
            if 'T' in fecha_manual:
                fecha_obj = datetime.fromisoformat(fecha_manual)
            else:
                fecha_obj = datetime.strptime(fecha_manual, '%Y-%m-%d %H:%M:%S')
        except Exception:
            fecha_obj = datetime.now()
    else:
        fecha_obj = datetime.now()

    conn = current_app.mysql.connection
    cursor = conn.cursor(DictCursor)

    try:
        # 1. Calcular total
        total = sum(item['cantidad'] * item['precio_unitario'] for item in items)

        # 2. Obtener usuario_id
        cursor.execute("SELECT id FROM usuarios WHERE uuid = %s", (usuario_uuid,))
        usuario = cursor.fetchone()
        if not usuario:
            raise ValueError("Usuario no encontrado")
        usuario_id = usuario['id']

        # 3. Crear pedido (sin cliente, venta directa de mostrador)
        pedido_uuid = str(uuidGenerado.uuid4())
        cursor.execute(
            """INSERT INTO pedidos (uuid, estado, total, usuario_id, usuario_uuid, fecha_hora)
               VALUES (%s, 'completado', %s, %s, %s, %s)""",
            (pedido_uuid, total, usuario_id, usuario_uuid, fecha_obj)
        )
        pedido_id = cursor.lastrowid

        # 4. Crear detalles y descontar inventario
        for item in items:
            ref_producto = item['ref_producto']
            cantidad = item['cantidad']
            precio_unitario = item['precio_unitario']
            subtotal = cantidad * precio_unitario

            # Obtener producto_id
            cursor.execute(
                "SELECT id FROM productos WHERE uuid = %s AND usuario_uuid = %s",
                (ref_producto, usuario_uuid)
            )
            producto = cursor.fetchone()
            if not producto:
                raise ValueError(f"Producto {ref_producto} no encontrado")
            producto_id = producto['id']

            # Verificar stock
            cursor.execute(
                "SELECT cantidad_actual FROM inventarios WHERE producto_id = %s",
                (producto_id,)
            )
            inv = cursor.fetchone()
            stock_actual = inv['cantidad_actual'] if inv else 0
            if stock_actual < cantidad:
                # Obtener nombre del producto para msg legible
                cursor.execute("SELECT nombre FROM productos WHERE id = %s", (producto_id,))
                nombre = cursor.fetchone()['nombre']
                raise ValueError(f"Stock insuficiente para '{nombre}'. Disponible: {stock_actual}, solicitado: {cantidad}")

            # Crear detalle
            cursor.execute(
                """INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario, subtotal, usuario_uuid)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (pedido_id, producto_id, cantidad, precio_unitario, subtotal, usuario_uuid)
            )

            # Descontar inventario
            cursor.execute(
                "UPDATE inventarios SET cantidad_actual = cantidad_actual - %s WHERE producto_id = %s",
                (cantidad, producto_id)
            )

        # Crear Factura Automáticamente
        factura_uuid = str(uuidGenerado.uuid4())
        numero_factura = f"FAC-{fecha_obj.strftime('%Y%m%d')}-{factura_uuid[:8]}"
        cursor.execute(
            """INSERT INTO facturas (uuid, numero_factura, total, estado, pedido_id, usuario_uuid, tipo, fecha_emision)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (factura_uuid, numero_factura, total, 'pagada', pedido_id, usuario_uuid, 'venta', fecha_obj)
        )

        conn.commit()

        return {
            "ref": pedido_uuid,
            "total": total,
            "items": len(items),
            "fecha": fecha_obj.isoformat()
        }

    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
