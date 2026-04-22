from flask import current_app
from MySQLdb.cursors import DictCursor
import uuid as uuidGenerado
from datetime import datetime

def registrar_compra_rapida(items, usuario_uuid, fecha_manual=None):
    """
    Registra compra: actualiza stock y CPP, crea pedido y factura de compra.
    items: lista de diccionarios con info del producto, cantidad, costo, etc.
    """
    # Determinar la fecha a usar
    if fecha_manual:
        try:
            # Intentar parsear ISO format (ej: 2026-04-22T09:55)
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
        # Calcular total solo de items q no sean "solo_stock"
        total = sum(item['cantidad'] * item['costo'] for item in items if not item.get('solo_stock'))

        cursor.execute("SELECT id FROM usuarios WHERE uuid = %s", (usuario_uuid,))
        usuario = cursor.fetchone()
        if not usuario:
            raise ValueError("Usuario no encontrado")
        usuario_id = usuario['id']

        # Crear pedido
        pedido_uuid = str(uuidGenerado.uuid4())
        cursor.execute(
            """INSERT INTO pedidos (uuid, estado, total, usuario_id, usuario_uuid, fecha_hora)
               VALUES (%s, 'completado', %s, %s, %s, %s)""",
            (pedido_uuid, total, usuario_id, usuario_uuid, fecha_obj)
        )
        pedido_id = cursor.lastrowid

        # Procesar items
        for item in items:
            ref_producto = item.get('ref_producto')
            cantidad = float(item['cantidad'])
            costo = float(item['costo'])
            solo_stock = item.get('solo_stock', False)

            n_nombre = item.get('nombre', 'Nuevo Producto')
            n_precio_venta = float(item.get('precio_venta', 0))
            n_categoria_uuid = item.get('ref_categoria')
            
            n_categoria_id = None
            if n_categoria_uuid:
                cursor.execute("SELECT id FROM categorias WHERE uuid = %s", (n_categoria_uuid,))
                cat = cursor.fetchone()
                if cat: n_categoria_id = cat['id']

            if not ref_producto:
                # Creación de nuevo producto
                ref_producto = str(uuidGenerado.uuid4())
                cursor.execute(
                    """INSERT INTO productos (uuid, nombre, precio_venta, costo_promedio, unidad_medida, categoria_id, usuario_uuid)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (ref_producto, n_nombre, n_precio_venta, costo, 'Unidad', n_categoria_id, usuario_uuid)
                )
                producto_id = cursor.lastrowid
                
                # Crear inventario en 0 (después se le sumará al final del ciclo)
                inv_uuid = str(uuidGenerado.uuid4())
                cursor.execute(
                    """INSERT INTO inventarios (uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (inv_uuid, producto_id, 0, 0, 10)
                )
            else:
                # Producto existente
                cursor.execute(
                    "SELECT id, costo_promedio FROM productos WHERE uuid = %s AND usuario_uuid = %s",
                    (ref_producto, usuario_uuid)
                )
                producto = cursor.fetchone()
                if not producto:
                    raise ValueError(f"Producto {ref_producto} no encontrado")
                
                producto_id = producto['id']
                
                # Obtener inventario actual para CPP si no es solo_stock
                nuevo_costo = float(producto['costo_promedio'] or 0)
                if not solo_stock:
                    cursor.execute("SELECT cantidad_actual FROM inventarios WHERE producto_id = %s", (producto_id,))
                    inv = cursor.fetchone()
                    
                    # Si no existe fila de inventario, la creamos
                    if not inv:
                        inv_uuid = str(uuidGenerado.uuid4())
                        cursor.execute(
                            "INSERT INTO inventarios (uuid, producto_id, cantidad_actual, cantidad_reservada, punto_reorden) VALUES (%s, %s, %s, %s, %s)",
                            (inv_uuid, producto_id, 0, 0, 10)
                        )
                        stock_actual = 0
                    else:
                        stock_actual = inv['cantidad_actual'] or 0
                        
                    costo_actual = float(producto['costo_promedio'] or 0)
                    if stock_actual + cantidad > 0:
                        valor_actual = stock_actual * costo_actual
                        valor_nuevo = cantidad * costo
                        nuevo_costo = (valor_actual + valor_nuevo) / (stock_actual + cantidad)
                    else:
                        nuevo_costo = costo

                # Actualizar producto existente
                cursor.execute(
                    """UPDATE productos SET nombre = %s, precio_venta = %s, costo_promedio = %s, categoria_id = %s
                       WHERE id = %s""",
                    (n_nombre, n_precio_venta, nuevo_costo, n_categoria_id, producto_id)
                )

            # Insertar detalle de pedido SOLAMENTE SI NO ES SOLO STOCK
            if not solo_stock:
                subtotal = cantidad * costo
                cursor.execute(
                    """INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario, subtotal, usuario_uuid)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (pedido_id, producto_id, cantidad, costo, subtotal, usuario_uuid)
                )

            # Actualizar inventario SIEMPRE
            cursor.execute(
                "UPDATE inventarios SET cantidad_actual = cantidad_actual + %s WHERE producto_id = %s",
                (cantidad, producto_id)
            )

        # Crear factura de compra (solo si el total no es 0 o podria ser cero)
        factura_uuid = str(uuidGenerado.uuid4())
        numero_factura = f"CMP-{fecha_obj.strftime('%Y%m%d')}-{factura_uuid[:8]}"
        cursor.execute(
            """INSERT INTO facturas (uuid, numero_factura, total, estado, pedido_id, usuario_uuid, tipo, fecha_emision)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (factura_uuid, numero_factura, total, 'pagada', pedido_id, usuario_uuid, 'compra', fecha_obj)
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
