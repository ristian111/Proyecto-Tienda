import { API_URL, getAuthHeaders } from './config';

export interface Product {
    ref: string;
    nombre: string;
    precio_venta: number | string;
    costo_promedio: number | string;
    unidad_medida: string;
    ref_categoria: string;
}

export interface Category {
    ref: string;
    nombre: string;
    descripcion: string;
}

export interface Invoice {
    ref: string;
    numero_factura: string;
    total: number;
    fecha_emision: string;
    estado: string;
    ref_pedido: string;
}

export interface Inventory {
    ref: string;
    cantidad_actual: number;
    cantidad_reservada: number;
    punto_reorden: number;
    ref_producto: string;
}

async function handleRes<T>(res: Response): Promise<T> {
    if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.mensaje || `Error ${res.status}`);
    }
    return res.json();
}

export const api = {

    login: async (username: string, password: string): Promise<{ token: string }> => {
        const res = await fetch(`${API_URL}/v1/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        return handleRes(res);
    },

    getProducts: async (): Promise<Product[]> => {
        const res = await fetch(`${API_URL}/v1/productos/`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    createProduct: async (data: {
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

    updateProduct: async (uuid: string, data: {
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

    deleteProduct: async (uuid: string) => {
        const res = await fetch(`${API_URL}/v1/productos/${uuid}`, {
            method: 'DELETE',
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    getCategories: async (): Promise<Category[]> => {
        const res = await fetch(`${API_URL}/v1/categorias/`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    createCategory: async (data: { nombre: string; descripcion: string }) => {
        const res = await fetch(`${API_URL}/v1/categorias/`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    updateCategory: async (uuid: string, data: { nombre: string; descripcion: string }) => {
        const res = await fetch(`${API_URL}/v1/categorias/${uuid}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    deleteCategory: async (uuid: string) => {
        const res = await fetch(`${API_URL}/v1/categorias/${uuid}`, {
            method: 'DELETE',
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    getInventories: async (): Promise<Inventory[]> => {
        const res = await fetch(`${API_URL}/v1/inventarios/`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    getInvoices: async (fechaInicio?: string, fechaFin?: string): Promise<Invoice[]> => {
        let url = `${API_URL}/v1/facturas/`;
        const params = new URLSearchParams();
        if (fechaInicio) params.append('fecha_inicio', fechaInicio);
        if (fechaFin) params.append('fecha_fin', fechaFin);
        if (params.toString()) url += `?${params.toString()}`;

        const res = await fetch(url, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    registerQuickSale: async (data: { fecha?: string; items: { ref_producto: string; cantidad: number; precio_unitario: number }[] }) => {
        const res = await fetch(`${API_URL}/v1/ventas/rapida`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    registerQuickPurchase: async (data: { fecha?: string; items: any[] }) => {
        const res = await fetch(`${API_URL}/v1/compras/rapida`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    registerQuickPedido: async (data: { fecha?: string; items: any[] }) => {
        const res = await fetch(`${API_URL}/v1/pedidos/rapida`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(data),
        });
        return handleRes(res);
    },

    getPendingPedidos: async (): Promise<any[]> => {
        const res = await fetch(`${API_URL}/v1/pedidos/pendientes`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    getPedidoDetails: async (pedidoUuid: string): Promise<any[]> => {
        const res = await fetch(`${API_URL}/v1/pedidos/${pedidoUuid}/detalles`, {
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    completePedido: async (pedidoUuid: string, presencial: boolean = true) => {
        const res = await fetch(`${API_URL}/v1/facturas/${pedidoUuid}?tipo=${presencial}`, {
            method: 'POST',
            headers: getAuthHeaders(),
        });
        return handleRes(res);
    },

    getTodaySummary: async () => {
        const res = await fetch(`${API_URL}/v1/estadisticas/resumen-hoy`, { headers: getAuthHeaders() });
        return handleRes<any>(res);
    },
    getTopProducts: async (filter: string = 'mensual') => {
        const res = await fetch(`${API_URL}/v1/estadisticas/top-productos?filtro=${filter}`, { headers: getAuthHeaders() });
        return handleRes<any>(res);
    },
    getRevenueProfit: async (days: number = 7) => {
        const res = await fetch(`${API_URL}/v1/estadisticas/ingresos-ganancias?dias=${days}`, { headers: getAuthHeaders() });
        return handleRes<any>(res);
    },
    getPeakHours: async () => {
        const res = await fetch(`${API_URL}/v1/estadisticas/horas-pico`, { headers: getAuthHeaders() });
        return handleRes<any>(res);
    },
    getStagnantProducts: async () => {
        const res = await fetch(`${API_URL}/v1/estadisticas/productos-estancados`, { headers: getAuthHeaders() });
        return handleRes<any>(res);
    },
    getCategoryPercentages: async () => {
        const res = await fetch(`${API_URL}/v1/estadisticas/porcentaje-categorias`, { headers: getAuthHeaders() });
        return handleRes<any>(res);
    }
};
