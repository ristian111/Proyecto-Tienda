import { api } from '../api/endpoints';

function getStatusBadge(status: string): string {
    const statusColors: Record<string, string> = {
        pagada: '#22c55e',
        emitida: '#eab308',
        anulada: '#ef4444',
    };
    const badgeColor = statusColors[status.toLowerCase()] || '#6b7280';
    return `<span class="badge invoice-status" style="background: ${badgeColor}20; color: ${badgeColor}; border: 1px solid ${badgeColor}40;">${status}</span>`;
}

let currentPageIndex = 1;
const itemsPerPageLimit = 50;

let storedInvoices: any[] = [];

let startDateFilter = '';
let endDateFilter = '';

export async function renderInvoices(container: HTMLElement) {

    container.innerHTML = `
        <div class="page-header">
            <h1>Historial Compra/Venta</h1>
        </div>

        <div class="filter-bar invoice-filters">
            <div class="filter-group">
                <label for="fecha-inicio">Desde:</label>
                <input type="date" id="fecha-inicio" value="${startDateFilter}" class="filter-input">
            </div>
            <div class="filter-group">
                <label for="fecha-fin">Hasta:</label>
                <input type="date" id="fecha-fin" value="${endDateFilter}" class="filter-input">
            </div>
            <div class="filter-actions">
                <button id="btn-filtrar" class="btn-primary">Filtrar</button>
                <button id="btn-limpiar" class="btn-secondary">Limpiar</button>
            </div>
        </div>
        
        <!-- FIX: We created a dedicated container JUST for the table/data -->
        <div id="data-container">
            <h2 class="loading-state">Cargando facturas...</h2>
        </div>
    `;

    document.getElementById('btn-filtrar')?.addEventListener('click', async () => {
        // Chapuza bien insana, carajo.
        let rawStart = (document.getElementById('fecha-inicio') as HTMLInputElement).value;
        let rawEnd = (document.getElementById('fecha-fin') as HTMLInputElement).value;

        if (!rawStart && rawEnd) {
            rawStart = '0666-01-01';
        }
        else if (rawStart && !rawEnd) {
            rawEnd = '7777-01-01';
        }

        startDateFilter = rawStart;
        endDateFilter = rawEnd;


        await renderInvoices(container);
    });

    document.getElementById('btn-limpiar')?.addEventListener('click', async () => {
        startDateFilter = '';
        endDateFilter = '';
        await renderInvoices(container);
    });

    const dataContainer = document.getElementById('data-container')!;

    try {
        storedInvoices = await api.getInvoices(startDateFilter, endDateFilter);

        if (storedInvoices.length === 0) {
            dataContainer.innerHTML = `
                <p class="empty-state-text">No hay facturas registradas aún.</p>
            `;
            return;
        }

        renderPage(dataContainer, 1);
    } catch (error) {
        dataContainer.innerHTML = '<h2 class="error-state">Error cargando facturas</h2><p class="error-hint">Verifica que el backend esté corriendo.</p>';
    }
}

function renderPage(dataContainer: HTMLElement, pageIndex: number) {
    currentPageIndex = pageIndex;
    const startIndex = (pageIndex - 1) * itemsPerPageLimit;
    const endIndex = startIndex + itemsPerPageLimit;

    const itemsToDisplay = storedInvoices.slice(startIndex, endIndex);
    const totalPageCount = Math.ceil(storedInvoices.length / itemsPerPageLimit);

    const rowsHTML = itemsToDisplay.map((invoice, index) => {
        const uniqueElementId = `factura-detalles-${startIndex + index}`;
        const invoiceTotal = Number(invoice.total) || 0;

        let detailsHTML = '';
        if (invoice.detalles && invoice.detalles.length > 0) {
            detailsHTML = invoice.detalles.map((detail: any) => `
                <div class="invoice-detail-line">
                    <span class="invoice-detail-name">${detail.nombre}</span>
                    <span class="invoice-detail-qty">${detail.cantidad} ud.</span>
                    <span class="invoice-detail-price">$${Number(detail.precio_unitario).toFixed(2)}</span>
                </div>
            `).join('');
        } else {
            detailsHTML = '<div class="invoice-detail-empty">No hay detalles registrados.</div>';
        }

        const formattedDate = new Date(invoice.fecha_emision).toLocaleString('es-MX', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });

        return `
            <tr class="hover-row" onclick="document.getElementById('${uniqueElementId}').classList.toggle('hidden')">
                <td class="invoice-row-number">${invoice.numero_factura}</td>
                <td><span class="invoice-items-badge">${invoice.cantidad_productos || 0} items</span></td>
                <td class="invoice-row-total">$${invoiceTotal.toFixed(2)}</td>
                <td class="invoice-row-date">${formattedDate}</td>
                <td>${getStatusBadge(invoice.estado)}</td>
            </tr>
            <tr id="${uniqueElementId}" class="hidden invoice-detail-row">
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

    dataContainer.innerHTML = `
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
            <button class="pagination-btn" id="btn-prev" ${currentPageIndex === 1 ? 'disabled' : ''}>&larr; Anterior</button>
            <span class="pagination-info">Página ${currentPageIndex} de ${totalPageCount || 1} <span class="pagination-count">(${storedInvoices.length} registros)</span></span>
            <button class="pagination-btn" id="btn-next" ${currentPageIndex >= totalPageCount ? 'disabled' : ''}>Siguiente &rarr;</button>
        </div>
    `;

    document.getElementById('btn-prev')?.addEventListener('click', () => {
        if (currentPageIndex > 1) renderPage(dataContainer, currentPageIndex - 1);
    });

    document.getElementById('btn-next')?.addEventListener('click', () => {
        if (currentPageIndex < totalPageCount) renderPage(dataContainer, currentPageIndex + 1);
    });
}