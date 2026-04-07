import { API_URL, getAuthHeaders } from './config';

// ─── Tipos ───────────────────────────────────────────────
export interface Producto {
    ref: string;       // uuid
    nombre: string;
    precio_venta: number | string;
    costo_promedio: number | string;
    unidad_medida: string;
    ref_categoria: string;
}

export interface Categoria {
    ref: string;
    nombre: string;
    descripcion: string;
}

export interface Factura {
    ref: string;
    numero_factura: string;
    total: number;
    fecha_emision: string;
    estado: string;
    ref_pedido: string;
}

export interface Inventario {
    ref: string;
    cantidad_actual: number;
    cantidad_reservada: number;
    punto_reorden: number;
    ref_producto: string;
}

// ─── Helper para manejar respuestas ──────────────────────
async function handleRes<T>(res: Response): Promise<T> {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.mensaje || `Error ${res.status}`);
    }
    return res.json();
}

// ─── API ─────────────────────────────────────────────────
export const api = {

    // ── Auth ──────────────────────────────────────────────
    login: async (username: string, password: string): Promise<{ token: string }> => {
        const res = await fetch(`${API_URL}/v1/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        return handleRes(res);
    },

    // ── Productos ─────────────────────────────────────────
    getProductos: async (): Promise<Producto[]> => {
        const res = await fetch(`${API_URL}/v1/productos/`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    createProducto: async (data: {
        nombre: string;
        precio_venta: number;
        costo_promedio: number;
        unidad_medida: string;
        ref_categoria: string;
        cantidad_actual: number;
    }) => {
        const res = await fetch(`${API_URL}/v1/productos/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    updateProducto: async (uuid: string, data: {
        nombre: string;
        precio_venta: number;
        costo_promedio: number;
        unidad_medida: string;
        ref_categoria: string;
    }) => {
        const res = await fetch(`${API_URL}/v1/productos/${uuid}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    deleteProducto: async (uuid: string) => {
        const res = await fetch(`${API_URL}/v1/productos/${uuid}`, {
            method: 'DELETE',
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    // ── Categorías ────────────────────────────────────────
    getCategorias: async (): Promise<Categoria[]> => {
        const res = await fetch(`${API_URL}/v1/categorias/`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    createCategoria: async (data: { nombre: string; descripcion: string }) => {
        const res = await fetch(`${API_URL}/v1/categorias/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    updateCategoria: async (uuid: string, data: { nombre: string; descripcion: string }) => {
        const res = await fetch(`${API_URL}/v1/categorias/${uuid}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    deleteCategoria: async (uuid: string) => {
        const res = await fetch(`${API_URL}/v1/categorias/${uuid}`, {
            method: 'DELETE',
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    // ── Inventarios ───────────────────────────────────────
    getInventarios: async (): Promise<Inventario[]> => {
        const res = await fetch(`${API_URL}/v1/inventarios/`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    // ── Facturas ──────────────────────────────────────────
    getFacturas: async (): Promise<Factura[]> => {
        const res = await fetch(`${API_URL}/v1/facturas/`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    // ── Ventas (POS) ─────────────────────────────────────
    registrarVentaRapida: async (items: { ref_producto: string; cantidad: number; precio_unitario: number }[]) => {
        const res = await fetch(`${API_URL}/v1/ventas/rapida`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ items }),
        });
        return handleRes(res);
    },

    // ── Compras ──────────────────────────────────────────
    registrarCompraRapida: async (items: any[]) => {
        const res = await fetch(`${API_URL}/v1/compras/rapida`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ items }),
        });
        return handleRes(res);
    },
};
