import { api } from '../api/endpoints';

function statusBadge(status: string): string {
    const colors: Record<string, string> = {
        pagada: '#22c55e',
        emitida: '#eab308',
        anulada: '#ef4444',
    };
    const color = colors[status.toLowerCase()] || '#6b7280';
    return `<span class="badge invoice-status" style="background: ${color}20; color: ${color}; border: 1px solid ${color}40;">${status}</span>`;
}

let currentPage = 1;
const itemsPerPage = 50;
let allInvoices: any[] = [];

export async function renderInvoices(container: HTMLElement) {
    container.innerHTML = '<h2 class="loading-state">Cargando facturas...</h2>';

    try {
        allInvoices = await api.getInvoices();

        if (allInvoices.length === 0) {
            container.innerHTML = `
                <div class="page-header"><h1>Facturas</h1></div>
                <p class="empty-state-text">No hay facturas registradas aún.</p>
            `;
            return;
        }

        renderPage(container, 1);
    } catch (error) {
        container.innerHTML = '<h2 class="error-state">Error cargando facturas</h2><p class="error-hint">Verifica que el backend esté corriendo.</p>';
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
                <div class="invoice-detail-line">
                    <span class="invoice-detail-name">${d.nombre}</span>
                    <span class="invoice-detail-qty">${d.cantidad} ud.</span>
                    <span class="invoice-detail-price">$${Number(d.precio_unitario).toFixed(2)}</span>
                </div>
            `).join('');
        } else {
            detailsHTML = '<div class="invoice-detail-empty">No hay detalles registrados.</div>';
        }

        const formattedDate = new Date(f.fecha_emision).toLocaleString('es-MX', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });

        return `
            <tr class="hover-row" onclick="document.getElementById('${uniqueId}').classList.toggle('hidden')">
                <td class="invoice-row-number">${f.numero_factura}</td>
                <td><span class="invoice-items-badge">${f.cantidad_productos || 0} items</span></td>
                <td class="invoice-row-total">$${total.toFixed(2)}</td>
                <td class="invoice-row-date">${formattedDate}</td>
                <td>${statusBadge(f.estado)}</td>
            </tr>
            <tr id="${uniqueId}" class="hidden invoice-detail-row">
                <td colspan="5">
                    <div class="invoice-detail-wrapper">
                        <h4 class="invoice-detail-header">
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
        <div class="page-header">
            <h1>Historial Compra/Venta (todavia no hay para ver compras)</h1>
        </div>
        <table class="invoice-table">
            <thead>
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
            <span class="pagination-info">Página ${currentPage} de ${totalPages || 1} <span class="pagination-count">(${allInvoices.length} registros)</span></span>
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
