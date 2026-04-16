import { api } from '../api/endpoints';

function statusBadge(status: string): string {
    const colors: Record<string, string> = {
        pagada: '#22c55e',
        emitida: '#eab308',
        anulada: '#ef4444',
    };
    const color = colors[status.toLowerCase()] || '#6b7280';
    return `<span class="badge" style="background: ${color}20; color: ${color}; border: 1px solid ${color}40; padding: 2px 10px; border-radius: 999px; font-size: 0.8rem; text-transform: capitalize;">${status}</span>`;
}

let currentPage = 1;
const itemsPerPage = 50;
let allInvoices: any[] = [];

export async function renderInvoices(container: HTMLElement) {
    container.innerHTML = '<h2 style="color: #4b5563; padding-top: 40px;">Cargando facturas...</h2>';

    try {
        allInvoices = await api.getInvoices();

        if (allInvoices.length === 0) {
            container.innerHTML = `
                <div class="page-header"><h1>Facturas</h1></div>
                <p style="color: #9ca3af; font-style: italic; padding: 20px;">No hay facturas registradas aún.</p>
            `;
            return;
        }

        renderPage(container, 1);
    } catch (error) {
        container.innerHTML = '<h2 style="color: #ef4444;">Error cargando facturas</h2><p style="color: #9ca3af;">Verifica que el backend esté corriendo.</p>';
    }
}

function renderPage(container: HTMLElement, page: number) {
    currentPage = page;
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const itemsToShow = allInvoices.slice(startIndex, endIndex);
    const totalPages = Math.ceil(allInvoices.length / itemsPerPage);

    const rowsHTML = itemsToShow.map((f, index) => {
        const uniqueId = `factura-detalles-${startIndex + index}`;
        const total = Number(f.total) || 0;

        let detailsHTML = '';
        if (f.detalles && f.detalles.length > 0) {
            detailsHTML = f.detalles.map((d: any) => `
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #374151; padding: 8px 0; color: #d1d5db;">
                    <span style="flex: 2; padding-right: 15px;">${d.nombre}</span>
                    <span style="flex: 1; text-align: center;">${d.cantidad} ud.</span>
                    <span style="flex: 1; text-align: right; color: #10b981;">$${Number(d.precio_unitario).toFixed(2)}</span>
                </div>
            `).join('');
        } else {
            detailsHTML = '<div style="color: #9ca3af; padding: 10px 0;">No hay detalles registrados.</div>';
        }

        const formattedDate = new Date(f.fecha_emision).toLocaleString('es-MX', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });

        return `
            <tr style="cursor: pointer; transition: background 0.2s;" class="hover-row" onclick="document.getElementById('${uniqueId}').classList.toggle('hidden')">
                <td style="font-weight: 500; color: #f3f4f6;">${f.numero_factura}</td>
                <td><span style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 2px 8px; border-radius: 999px; font-weight: 600;">${f.cantidad_productos || 0} items</span></td>
                <td style="font-weight: 600;">$${total.toFixed(2)}</td>
                <td style="color: #9ca3af;">${formattedDate}</td>
                <td>${statusBadge(f.estado)}</td>
            </tr>
            <tr id="${uniqueId}" class="hidden" style="background: #111827;">
                <td colspan="5" style="padding: 0; border-bottom: 1px solid #1f2937;">
                    <div style="padding: 15px 30px; border-left: 3px solid #3b82f6;">
                        <h4 style="color: #9ca3af; margin-bottom: 10px; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 8px;">
                            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
                            Detalle de la Venta
                        </h4>
                        ${detailsHTML}
                    </div>
                </td>
            </tr>
        `;
    }).join('');

    container.innerHTML = `
        <style>
            .hover-row:hover { background: #374151 !important; }
            .hidden { display: none !important; }
            .pagination-btn { padding: 8px 16px; background: #374151; color: white; border: none; border-radius: 6px; cursor: pointer; transition: 0.2s; font-weight: 500; }
            .pagination-btn:hover:not(:disabled) { background: #4b5563; }
            .pagination-btn:disabled { opacity: 0.5; cursor: not-allowed; }
            .pagination-controls { display: flex; justify-content: space-between; align-items: center; margin-top: 25px; padding: 15px 20px; background: #1f2937; border-radius: 8px; border: 1px solid #374151; }
        </style>
        <div class="page-header">
            <h1>Historial Compra/Venta (todavia no hay para ver compras)</h1>
        </div>
        <table style="width: 100%; border-collapse: collapse; background: #1f2937; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
            <thead style="background: rgba(0,0,0,0.2);">
                <tr>
                    <th>Nº Factura</th>
                    <th>Productos</th>
                    <th>Total</th>
                    <th>Fecha Registro</th>
                    <th>Estado</th>
                </tr>
            </thead>
            <tbody>
                ${rowsHTML}
            </tbody>
        </table>
        
        <div class="pagination-controls">
            <button class="pagination-btn" id="btn-prev" ${currentPage === 1 ? 'disabled' : ''}>&larr; Anterior</button>
            <span style="color: #d1d5db; font-weight: 500;">Página ${currentPage} de ${totalPages || 1} <span style="color:#6b7280; font-size: 0.85em; margin-left: 8px;">(${allInvoices.length} registros)</span></span>
            <button class="pagination-btn" id="btn-next" ${currentPage >= totalPages ? 'disabled' : ''}>Siguiente &rarr;</button>
        </div>
    `;

    document.getElementById('btn-prev')?.addEventListener('click', () => {
        if (currentPage > 1) renderPage(container, currentPage - 1);
    });

    document.getElementById('btn-next')?.addEventListener('click', () => {
        if (currentPage < totalPages) renderPage(container, currentPage + 1);
    });
}
