import { api } from '../api/endpoints';

interface ProductWithStock {
    ref: string;
    nombre: string;
    precio_venta: number;
    stock: number;
}

interface CartItem {
    ref: string;
    nombre: string;
    precio: number;
    cantidad: number;
}

let globalInventory: ProductWithStock[] = [];
let cart: CartItem[] = [];
let pendingOrders: any[] = [];

function renderCart() {
    const tbody = document.getElementById('tabla-pedido-carrito')!;
    const spanTotal = document.getElementById('total-pedido')!;
    const btnCharge = document.getElementById('btn-registrar-pedido') as HTMLButtonElement;

    let total = 0;

    tbody.innerHTML = cart.map((item, index) => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;

        return `
            <tr>
                <td class="cell-name">${item.nombre}</td>
                <td>$${Number(item.precio).toFixed(2)}</td>
                <td>
                    <div class="qty-controls">
                        <button class="btn-qty btn-restar" data-index="${index}">−</button>
                        <span class="qty-value">${item.cantidad}</span>
                        <button class="btn-qty btn-sumar" data-index="${index}">+</button>
                    </div>
                </td>
                <td class="cell-stock">${subtotal.toFixed(2)}</td>
                <td>
                    <button class="btn btn-danger btn-sm btn-eliminar-carrito" data-index="${index}">
                        <i class='bx bx-x fs-icon'></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');

    if (spanTotal) spanTotal.textContent = total.toFixed(2);

    if (btnCharge) {
        btnCharge.disabled = cart.length === 0;
        btnCharge.style.opacity = cart.length === 0 ? '0.5' : '1';
    }
}

function renderPendingOrders() {
    const container = document.getElementById('pending-orders-container');
    if (!container) return;

    if (pendingOrders.length === 0) {
        container.innerHTML = `<p class="pos-hint">No hay pedidos pendientes actualmente.</p>`;
        return;
    }

    container.innerHTML = `
        <table class="compra-table">
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Cliente</th>
                    <th>Estado</th>
                    <th>Total</th>
                    <th>Acción</th>
                </tr>
            </thead>
            <tbody>
                ${pendingOrders.map(po => `
                    <tr class="pedido-row" style="cursor: pointer; transition: background 0.2s;" data-uuid="${po.id_pedido}">
                        <td>${new Date(po.hora_pedido).toLocaleString()}</td>
                        <td>${po.nombre_cliente}</td>
                        <td><span class="badge badge-warning">${po.estado_pedido}</span></td>
                        <td>$${Number(po.total).toFixed(2)}</td>
                        <td>
                            <button class="btn btn-success btn-sm btn-complete-order" data-uuid="${po.id_pedido}" title="Completar y Generar Factura">
                                <i class='bx bx-check'></i> Completar
                            </button>
                        </td>
                    </tr>
                    <tr class="details-row" id="row-det-${po.id_pedido}" style="display: none;">
                        <td colspan="5" style="padding: 0; background: var(--bg-hover);">
                            <div id="detalles-${po.id_pedido}" style="padding: 16px;">
                                <i class='bx bx-loader-alt bx-spin'></i> Cargando detalles...
                            </div>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

export async function renderPedidos(container: HTMLElement) {
    cart = [];
    globalInventory = [];
    pendingOrders = [];

    container.innerHTML = '<h2 class="loading-state">Cargando datos...</h2>';

    try {
        const [products, inventories, pending] = await Promise.all([
            api.getProducts(),
            api.getInventories(),
            api.getPendingPedidos()
        ]);

        pendingOrders = pending;
        const stockMap: Record<string, number> = {};
        inventories.forEach(inv => { stockMap[inv.ref_producto] = inv.cantidad_actual; });

        globalInventory = products.map(p => ({
            ref: p.ref,
            nombre: p.nombre,
            precio_venta: Number(p.precio_venta),
            stock: stockMap[p.ref] ?? 0,
        }));

        container.innerHTML = `
            <div class="page-header">
                <h1><i class='bx bx-cart text-accent mr-6'></i>Pedidos</h1>
                <div class="header-actions">
                    <input type="datetime-local" id="pedido-fecha" class="pos-input-edit" title="Fecha del pedido" />
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 24px;">
                <div style="width: 100%;">
                    <h3>Nuevo Pedido</h3>
                    
                    <div class="pos-search-wrapper">
                        <i class='bx bx-search pos-search-icon'></i>
                        <input type="text" id="buscador-productos" placeholder="Buscar producto..." autocomplete="off">
                        <div id="dropdown-resultados" class="pos-dropdown"></div>
                    </div>

                    <div id="carrito-vacio" class="pos-empty-state">
                        <i class='bx bx-cart empty-icon'></i>
                        <p>Agrega productos usando el buscador</p>
                    </div>

                    <table id="tabla-pedido" style="display: none; width: 100%;">
                        <thead>
                            <tr>
                                <th>Producto</th>
                                <th>Precio</th>
                                <th>Cantidad</th>
                                <th>Subtotal</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody id="tabla-pedido-carrito"></tbody>
                    </table>

                    <div class="pos-footer" style="margin-top: 16px;">
                        <div class="pos-total">
                            Total: <span class="pos-total-amount">$<span id="total-pedido">0.00</span></span>
                        </div>
                        <button id="btn-registrar-pedido" class="btn pos-btn-cobrar" disabled style="opacity: 0.5;">
                            <i class='bx bx-plus-circle fs-icon-lg'></i>
                            Registrar Pedido
                        </button>
                    </div>

                    <div id="pedido-feedback" class="pos-feedback" style="display: none; margin-top:16px;"></div>
                </div>
                
                <div id="pedidos-pendientes-section" style="width: 100%; background: var(--bg-card); padding: 16px; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <h3 style="margin: 0;">Pedidos Pendientes</h3>
                        <button id="btn-refresh-pending" class="btn btn-sm"><i class='bx bx-refresh'></i></button>
                    </div>
                    <div id="pending-orders-container"></div>
                </div>
            </div>
        `;

        renderPendingOrders();

        const dateInput = document.getElementById('pedido-fecha') as HTMLInputElement;
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        if (dateInput) dateInput.value = now.toISOString().slice(0, 16);

        const searchInput = document.getElementById('buscador-productos') as HTMLInputElement;
        const dropdown = document.getElementById('dropdown-resultados')!;

        searchInput.addEventListener('input', () => {
            const text = searchInput.value.toLowerCase().trim();
            if (text.length === 0) {
                dropdown.style.display = 'none';
                return;
            }

            const results = globalInventory.filter(p => p.nombre.toLowerCase().includes(text)).slice(0, 10);

            if (results.length > 0) {
                dropdown.innerHTML = results.map(p => {
                    return `
                    <div class="pos-dropdown-item" data-id="${p.ref}">
                        <span class="pos-dropdown-name">${p.nombre}</span>
                        <span class="pos-dropdown-meta">
                            <span class="text-success">$${p.precio_venta.toFixed(2)}</span>
                        </span>
                    </div>`;}).join('');
                dropdown.style.display = 'block';
            } else {
                dropdown.innerHTML = `<div class="pos-dropdown-item pos-dropdown-empty">Nada por aqui</div>`;
                dropdown.style.display = 'block';
            }
        });

        dropdown.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            const itemDiv = target.closest('.pos-dropdown-item') as HTMLElement;
            if (!itemDiv || itemDiv.classList.contains('pos-dropdown-empty')) return;

            const productId = itemDiv.getAttribute('data-id');
            const product = globalInventory.find(p => p.ref === productId);

            if (product) {
                const inCart = cart.find(item => item.ref === product.ref);
                if (inCart) {
                    inCart.cantidad += 1;
                } else {
                    cart.push({
                        ref: product.ref,
                        nombre: product.nombre,
                        precio: product.precio_venta,
                        cantidad: 1,
                    });
                }
                searchInput.value = '';
                dropdown.style.display = 'none';
                searchInput.focus();

                updateTable();
                renderCart();
            }
        });

        document.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            if (target.closest('.pos-search-wrapper') === null) {
                if (dropdown) dropdown.style.display = 'none';
            }
        });

        document.getElementById('pedidos-pendientes-section')?.addEventListener('click', async (e) => {
            const target = e.target as HTMLElement;

            const row = target.closest('.pedido-row') as HTMLElement;
            if (row && !target.closest('.btn-complete-order')) {
                const uuid = row.dataset.uuid;
                if (!uuid) return;
                
                const detailsRow = document.getElementById(`row-det-${uuid}`);
                const detailsContainer = document.getElementById(`detalles-${uuid}`);
                
                if (detailsRow) {
                    if (detailsRow.style.display === 'none') {
                        detailsRow.style.display = 'table-row';
                        if (detailsContainer && !detailsContainer.dataset.loaded) {
                            try {
                                const dets = await api.getPedidoDetails(uuid);
                                detailsContainer.innerHTML = `
                                    <h4 style="margin-top:0; margin-bottom: 12px; color: var(--accent);">Detalles del Pedido</h4>
                                    <table class="compra-table" style="background: var(--bg-card); width: 100%; border-radius: 6px; overflow: hidden;">
                                        <thead style="background: var(--bg-main);"><tr><th style="padding: 8px;">Producto</th><th style="padding: 8px;">Cantidad</th><th style="padding: 8px;">Precio U.</th><th style="padding: 8px;">Subtotal</th></tr></thead>
                                        <tbody>
                                            ${dets.map(d => `
                                                <tr>
                                                    <td style="padding: 8px;">${d.producto_nombre}</td>
                                                    <td style="padding: 8px;">${Number(d.cantidad).toFixed(2)}</td>
                                                    <td style="padding: 8px;">$${Number(d.precio_unitario).toFixed(2)}</td>
                                                    <td style="padding: 8px;">$${Number(d.subtotal).toFixed(2)}</td>
                                                </tr>
                                            `).join('')}
                                        </tbody>
                                        <tfoot style="background: var(--bg-main);">
                                            <tr>
                                                <td colspan="3" style="text-align: right; font-weight: bold; padding: 8px;">Total:</td>
                                                <td style="font-weight: bold; padding: 8px;">$${Number(dets.reduce((acc, curr) => acc + Number(curr.subtotal), 0)).toFixed(2)}</td>
                                            </tr>
                                        </tfoot>
                                    </table>
                                `;
                                detailsContainer.dataset.loaded = "true";
                            } catch (err) {
                                detailsContainer.innerHTML = '<span class="text-error"><i class="bx bx-error"></i> Error cargando detalles</span>';
                            }
                        }
                    } else {
                        detailsRow.style.display = 'none';
                    }
                }
                return;
            }

            const btnComplete = target.closest('.btn-complete-order') as HTMLElement;
            if (btnComplete) {
                const uuid = btnComplete.dataset.uuid;
                if (!uuid) return;
                try {
                    btnComplete.innerHTML = "<i class='bx bx-loader-alt bx-spin'></i>";
                    btnComplete.style.pointerEvents = "none";
                    await api.completePedido(uuid, true);
                    const pending = await api.getPendingPedidos();
                    pendingOrders = pending;
                    renderPendingOrders();
                    
                    const feedback = document.getElementById('pedido-feedback');
                    if (feedback) {
                        feedback.className = 'pos-feedback pos-feedback-success';
                        feedback.innerHTML = `<i class='bx bx-check-circle'></i> Pedido completado, factura generada y stock descontado.`;
                        feedback.style.display = 'flex';
                        setTimeout(() => feedback.style.display = 'none', 4000);
                    }
                } catch(err: any) {
                    alert("Error completando el pedido: " + (err.message || 'Desconocido'));
                    btnComplete.innerHTML = "<i class='bx bx-check'></i> Completar";
                    btnComplete.style.pointerEvents = "auto";
                }
            }

            if (target.closest('#btn-refresh-pending')) {
                const pending = await api.getPendingPedidos();
                pendingOrders = pending;
                renderPendingOrders();
            }
        });

        document.getElementById('tabla-pedido-carrito')!.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            const btn = target.closest('[data-index]') as HTMLElement;
            if (!btn) return;

            const index = parseInt(btn.getAttribute('data-index') || '-1');
            if (index === -1) return;

            if (btn.classList.contains('btn-sumar')) {
                cart[index].cantidad += 1;
            } else if (btn.classList.contains('btn-restar')) {
                cart[index].cantidad -= 1;
                if (cart[index].cantidad <= 0) cart.splice(index, 1);
            } else if (btn.classList.contains('btn-eliminar-carrito')) {
                cart.splice(index, 1);
            }

            updateTable();
            renderCart();
        });

        document.getElementById('btn-registrar-pedido')!.addEventListener('click', async () => {
            if (cart.length === 0) return;

            const btnCharge = document.getElementById('btn-registrar-pedido') as HTMLButtonElement;
            const feedback = document.getElementById('pedido-feedback')!;

            btnCharge.disabled = true;
            btnCharge.innerHTML = `<i class='bx bx-loader-alt bx-spin fs-icon-lg'></i> Procesando...`;

            try {
                const fechaSeleccionada = (document.getElementById('pedido-fecha') as HTMLInputElement)?.value;
                const itemsPayload = cart.map(item => ({
                    ref_producto: item.ref,
                    cantidad: item.cantidad,
                    precio_unitario: item.precio,
                }));

                await api.registerQuickPedido({
                    fecha: fechaSeleccionada,
                    items: itemsPayload
                });

                cart = [];
                updateTable();
                renderCart();

                pendingOrders = await api.getPendingPedidos();
                renderPendingOrders();

                feedback.className = 'pos-feedback pos-feedback-success';
                feedback.innerHTML = `<i class='bx bx-check-circle'></i> Pedido registrado en estado 'pendiente'.`;
                feedback.style.display = 'flex';
                setTimeout(() => feedback.style.display = 'none', 4000);
            } catch (err: any) {
                feedback.className = 'pos-feedback pos-feedback-error';
                feedback.innerHTML = `<i class='bx bx-error-circle'></i> ${err.message || 'Error al registrar pedido'}`;
                feedback.style.display = 'flex';
                setTimeout(() => feedback.style.display = 'none', 5000);
            } finally {
                btnCharge.disabled = cart.length === 0;
                btnCharge.style.opacity = cart.length === 0 ? '0.5' : '1';
                btnCharge.innerHTML = `<i class='bx bx-plus-circle fs-icon-lg'></i> Registrar Pedido`;
            }
        });

    } catch (error) {
        container.innerHTML = '<h2 class="error-state">Error cargando datos</h2>';
    }
}

function updateTable() {
    const table = document.getElementById('tabla-pedido');
    const empty = document.getElementById('carrito-vacio');
    if (cart.length > 0) {
        if (table) table.style.display = '';
        if (empty) empty.style.display = 'none';
    } else {
        if (table) table.style.display = 'none';
        if (empty) empty.style.display = '';
    }
}
