-- SQL Migration to add user isolation
-- Agregar columna usuario_uuid a las tablas necesarias
ALTER TABLE productos ADD COLUMN usuario_uuid VARCHAR(36) NULL;
ALTER TABLE clientes ADD COLUMN usuario_uuid VARCHAR(36) NULL;
ALTER TABLE pedidos ADD COLUMN usuario_uuid VARCHAR(36) NULL;
ALTER TABLE facturas ADD COLUMN usuario_uuid VARCHAR(36) NULL;
ALTER TABLE detalle_pedido ADD COLUMN usuario_uuid VARCHAR(36) NULL;

-- Fix missing fecha_hora column in pedidos to allow statistics queries to work
ALTER TABLE pedidos ADD COLUMN fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- inventarios shares isolation through producto_id, so it doesn't strictly need usuario_uuid for direct isolation,
-- but the queries will join with productos to filter by usuario_uuid.
