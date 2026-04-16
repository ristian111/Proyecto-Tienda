import { api } from '../api/endpoints';
import type { Product, Category } from '../api/endpoints';

interface PurchaseProductInfo {
    ref?: string;
    nombre: string;
    costo: number;
    precio_venta: number;
    cantidad: number;
    ref_categoria?: string;
    solo_stock: boolean;
}

let globalInventory: (Product & { stock: number })[] = [];
let globalCategories: Category[] = [];
let purchaseCart: PurchaseProductInfo[] = [];

function renderPurchaseCart() {
    const tbody = document.getElementById('tabla-compras-carrito')!;
    const spanTotal = document.getElementById('total-compra')!;
    const btnRegister = document.getElementById('btn-registrar-compra') as HTMLButtonElement;

    let total = 0;

    tbody.innerHTML = purchaseCart.map((item, index) => {
        if (!item.solo_stock) {
            total += item.costo * item.cantidad;
        }

        const categoryOptions = globalCategories.map(c =>
            `<option value="${c.ref}" ${c.ref === item.ref_categoria ? 'selected' : ''}>${c.nombre}</option>`
        ).join('');

        const isNew = !item.ref;

        return `
            <tr class="compra-row ${item.solo_stock ? 'compra-row--solo-stock' : ''}">
                <td>
                    <div style="display:flex;align-items:center;gap:6px;">
                        ${isNew ? '<span style="background:#6366f1;color:#fff;font-size:0.6rem;padding:1px 5px;border-radius:4px;font-weight:600;white-space:nowrap;">NUEVO</span>' : ''}
                        <input type="text" class="pos-input-edit compra-input" data-field="nombre" data-index="${index}" value="${item.nombre}" placeholder="Nombre del producto" style="width:100%; box-sizing:border-box; min-width:0;" />
                    </div>
                </td>
                <td>
                    <select class="pos-input-edit compra-select" data-field="ref_categoria" data-index="${index}" style="width:100%; box-sizing:border-box; min-width:0;">
                        <option value="">—</option>
                        ${categoryOptions}
                    </select>
                </td>
                <td>
                    <div class="compra-price-cell" style="display:flex; align-items:center; gap:4px;">
                        <span class="compra-dollar" style="margin:0; line-height:1; display:flex; align-items:center;">$</span>
                        <input type="number" step="0.01" min="0" class="pos-input-edit compra-input compra-input--num" data-field="costo" data-index="${index}" value="${item.costo}" ${item.solo_stock ? 'disabled' : ''} style="width:100%; box-sizing:border-box; min-width:0;" />
                    </div>
                </td>
                <td>
                    <div class="compra-price-cell" style="display:flex; align-items:center; gap:4px;">
                        <span class="compra-dollar" style="margin:0; line-height:1; display:flex; align-items:center;">$</span>
                        <input type="number" step="0.01" min="0" class="pos-input-edit compra-input compra-input--num" data-field="precio_venta" data-index="${index}" value="${item.precio_venta}" style="width:100%; box-sizing:border-box; min-width:0;" />
                    </div>
                </td>
                <td>
                    <input type="number" min="1" step="1" class="pos-input-edit compra-input compra-input--qty" data-field="cantidad" data-index="${index}" value="${item.cantidad}" style="width:100%; box-sizing:border-box; min-width:0;" />
                </td>
                <td style="text-align:center;">
                    <label class="compra-checkbox-label" style="display:flex; align-items:center; justify-content:center; gap:6px; margin:0; cursor:pointer;">
                        <input type="checkbox" class="pos-input-checkbox" data-index="${index}" ${item.solo_stock ? 'checked' : ''} style="margin:0;" />
                        <span style="white-space:nowrap;">Solo stock</span>
                    </label>
                </td>
                <td style="text-align:center;">
                    <button class="btn btn-danger btn-sm btn-eliminar-compra" data-index="${index}" title="Quitar">
                        <i class='bx bx-x' style="font-size:1.1rem;"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');

    spanTotal.textContent = total.toFixed(2);

    if (btnRegister) {
        btnRegister.disabled = purchaseCart.length === 0;
        btnRegister.style.opacity = purchaseCart.length === 0 ? '0.5' : '1';
    }
}

function hasDuplicates(): string | null {
    const names = purchaseCart.map(c => c.nombre.trim().toLowerCase());
    const seen = new Set<string>();
    for (const n of names) {
        if (seen.has(n)) return n;
        seen.add(n);
    }
    return null;
}

function addExistingProduct(product: Product & { stock: number }) {
    const alreadyExists = purchaseCart.find(c => c.ref === product.ref);
    if (!alreadyExists) {
        purchaseCart.push({
            ref: product.ref,
            nombre: product.nombre,
            costo: Number(product.costo_promedio),
            precio_venta: Number(product.precio_venta),
            ref_categoria: product.ref_categoria,
            cantidad: 1,
            solo_stock: false
        });
    } else {
        alreadyExists.cantidad += 1;
    }
}

function addNewProduct(baseName: string) {
    const exists = purchaseCart.some(c => c.nombre.trim().toLowerCase() === baseName.trim().toLowerCase());
    if (exists) return;

    purchaseCart.push({
        nombre: baseName || 'Nuevo Producto',
        costo: 0,
        precio_venta: 0,
        cantidad: 1,
        solo_stock: false
    });
}

export async function renderPurchases(container: HTMLElement) {
    purchaseCart = [];
    globalInventory = [];
    globalCategories = [];

    container.innerHTML = '<h2 style="color: #4b5563; padding-top: 40px;">Cargando inventario...</h2>';

    try {
        const [products, inventories, categories] = await Promise.all([
            api.getProducts(),
            api.getInventories(),
            api.getCategories(),
        ]);

        globalCategories = categories;
        const stockMap: Record<string, number> = {};
        inventories.forEach(inv => stockMap[inv.ref_producto] = inv.cantidad_actual);

        globalInventory = products.map(p => ({
            ...p,
            stock: stockMap[p.ref] ?? 0,
            costo_promedio: Number(p.costo_promedio || 0),
            precio_venta: Number(p.precio_venta || 0)
        }));

        container.innerHTML = `
            <div class="page-header">
                <h1><i class='bx bx-archive-in' style="color: #10b981; margin-right: 8px;"></i>Registrar Compra</h1>
            </div>

            <div class="pos-search-wrapper" style="margin-top: 12px;">
                <i class='bx bx-search pos-search-icon'></i>
                <input
                    type="text"
                    id="buscador-compras"
                    placeholder="Buscar producto existente (Enter) · Crear nuevo (Shift + Enter)"
                    autocomplete="off"
                >
                <div id="dropdown-compras" class="pos-dropdown"></div>
            </div>

            <div id="compras-vacio" class="pos-empty-state">
                <i class='bx bx-box' style="font-size: 2.8rem; color: #374151;"></i>
                <p style="margin:8px 0 2px; font-size:0.95rem;">Busca un producto y presiona <kbd style="background:#374151;padding:2px 6px;border-radius:4px;font-size:0.8rem;">Enter</kbd> para agregarlo</p>
                <small style="color: #6b7280;">o <kbd style="background:#374151;padding:2px 6px;border-radius:4px;font-size:0.75rem;">Shift + Enter</kbd> para crear uno nuevo con ese nombre</small>
            </div>

            <div style="overflow-x: auto; margin-top: 1rem; width: 100%;">
                <table id="tabla-compras" class="compra-table" style="display: none; width: 100%; table-layout: fixed; min-width: 900px;">
                    <thead>
                        <tr>
                            <th style="width:25%;">Producto</th>
                            <th style="width:15%;">Categoría</th>
                            <th style="width:14%;">Costo Un.</th>
                            <th style="width:14%;">P. Venta</th>
                            <th style="width:10%;">Cant.</th>
                            <th style="width:14%;">Opción</th>
                            <th style="width:8%;"></th>
                        </tr>
                    </thead>
                    <tbody id="tabla-compras-carrito"></tbody>
                </table>
            </div>

            <div class="pos-footer">
                <div class="pos-total">
                    Total Inversión: <span class="pos-total-amount" style="color: #10b981;">$<span id="total-compra">0.00</span></span>
                </div>
                <button id="btn-registrar-compra" class="btn pos-btn-cobrar" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" disabled>
                    <i class='bx bx-save' style="font-size: 1.1rem;"></i>
                    Registrar Compra
                </button>
            </div>

            <div id="compra-feedback" class="pos-feedback" style="display: none;"></div>
        `;

        const searchInput = document.getElementById('buscador-compras') as HTMLInputElement;
        const dropdown = document.getElementById('dropdown-compras')!;
        searchInput.focus();

        searchInput.addEventListener('input', () => {
            const text = searchInput.value.toLowerCase().trim();
            if (!text) { dropdown.style.display = 'none'; return; }

            const results = globalInventory.filter(p => p.nombre.toLowerCase().includes(text)).slice(0, 10);

            if (results.length > 0) {
                dropdown.innerHTML = results.map(p => `
                    <div class="pos-dropdown-item" data-id="${p.ref}">
                        <span class="pos-dropdown-name">${p.nombre}</span>
                        <span class="pos-dropdown-meta">
                            <span style="color: #9ca3af;">Stock: ${p.stock}</span>
                            <span style="color: #10b981;">CPP: $${Number(p.costo_promedio).toFixed(2)}</span>
                        </span>
                    </div>
                `).join('');
                dropdown.style.display = 'block';
            } else {
                dropdown.innerHTML = `<div class="pos-dropdown-item pos-dropdown-empty">Sin coincidencias — presiona <b>Shift+Enter</b> para crear</div>`;
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
                addExistingProduct(product);
                searchInput.value = '';
                dropdown.style.display = 'none';
                searchInput.focus();
                updateVisibility();
                renderPurchaseCart();
            }
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const text = searchInput.value.trim();
                if (!text) return;

                if (e.shiftKey) {
                    const existsInCart = purchaseCart.some(c => c.nombre.trim().toLowerCase() === text.toLowerCase());
                    const existsInInventory = globalInventory.some(p => p.nombre.trim().toLowerCase() === text.toLowerCase());
                    if (existsInCart || existsInInventory) {
                        showFeedback('error', `Ya existe un producto con el nombre "${text}"`);
                        return;
                    }
                    addNewProduct(text);
                } else {
                    const firstItem = dropdown.querySelector('.pos-dropdown-item:not(.pos-dropdown-empty)') as HTMLElement;
                    if (firstItem) {
                        firstItem.click();
                        return;
                    }
                }

                searchInput.value = '';
                dropdown.style.display = 'none';
                searchInput.focus();
                updateVisibility();
                renderPurchaseCart();
            }
        });

        document.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            if (!target.closest('.pos-search-wrapper')) {
                dropdown.style.display = 'none';
            }
        });

        document.getElementById('tabla-compras')!.addEventListener('change', (e) => {
            const target = e.target as HTMLInputElement | HTMLSelectElement;
            const index = target.getAttribute('data-index');
            if (index === null) return;
            const i = parseInt(index);

            if (target.classList.contains('pos-input-edit')) {
                const field = target.getAttribute('data-field') as keyof PurchaseProductInfo;
                if (field === 'cantidad' || field === 'costo' || field === 'precio_venta') {
                    (purchaseCart[i] as any)[field] = parseFloat(target.value) || 0;
                } else if (field === 'nombre') {
                    const newName = target.value.trim().toLowerCase();
                    const dupInCart = purchaseCart.some((c, ci) => ci !== i && c.nombre.trim().toLowerCase() === newName);
                    const dupInInventory = globalInventory.some(p =>
                        p.ref !== purchaseCart[i].ref && p.nombre.trim().toLowerCase() === newName
                    );
                    if (dupInCart || dupInInventory) {
                        showFeedback('error', `Ya existe un producto con ese nombre`);
                        target.value = purchaseCart[i].nombre;
                        return;
                    }
                    purchaseCart[i].nombre = target.value;
                } else {
                    (purchaseCart[i] as any)[field] = target.value;
                }
                renderPurchaseCart();
            } else if (target.classList.contains('pos-input-checkbox')) {
                purchaseCart[i].solo_stock = (target as HTMLInputElement).checked;
                renderPurchaseCart();
            }
        });

        document.getElementById('tabla-compras')!.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            const btn = target.closest('.btn-eliminar-compra');
            if (btn) {
                const index = parseInt(btn.getAttribute('data-index') || '0');
                purchaseCart.splice(index, 1);
                updateVisibility();
                renderPurchaseCart();
            }
        });

        document.getElementById('btn-registrar-compra')!.addEventListener('click', async () => {
            if (purchaseCart.length === 0) return;

            const dup = hasDuplicates();
            if (dup) {
                showFeedback('error', `Hay nombres duplicados en la lista: "${dup}"`);
                return;
            }

            const btnReg = document.getElementById('btn-registrar-compra') as HTMLButtonElement;

            btnReg.disabled = true;
            btnReg.innerHTML = `<i class='bx bx-loader-alt bx-spin'></i> Procesando...`;

            try {
                const payload = purchaseCart.map(c => ({
                    ref_producto: c.ref || null,
                    nombre: c.nombre,
                    costo: c.costo,
                    precio_venta: c.precio_venta,
                    ref_categoria: c.ref_categoria,
                    cantidad: c.cantidad,
                    solo_stock: c.solo_stock
                }));

                const result: any = await api.registerQuickPurchase(payload);

                purchaseCart = [];
                updateVisibility();
                renderPurchaseCart();

                await reloadInventorySilent();

                showFeedback('success', `${result.mensaje} — Total: $${(result.compra?.total ?? 0).toFixed(2)}`);

            } catch (err: any) {
                showFeedback('error', err.message || 'Error al registrar');
            } finally {
                btnReg.disabled = purchaseCart.length === 0;
                btnReg.style.opacity = purchaseCart.length === 0 ? '0.5' : '1';
                btnReg.innerHTML = `<i class='bx bx-save' style="font-size: 1.1rem;"></i> Registrar Compra`;
            }
        });

        function showFeedback(type: 'success' | 'error', msg: string) {
            const feedback = document.getElementById('compra-feedback')!;
            feedback.className = `pos-feedback pos-feedback-${type}`;
            const icon = type === 'success' ? 'bx-check-circle' : 'bx-error-circle';
            feedback.innerHTML = `<i class='bx ${icon}'></i> ${msg}`;
            feedback.style.display = 'flex';
            setTimeout(() => feedback.style.display = 'none', 5000);
        }

        async function reloadInventorySilent() {
            const [prods, invs] = await Promise.all([api.getProducts(), api.getInventories()]);
            const stkMap: Record<string, number> = {};
            invs.forEach(inv => stkMap[inv.ref_producto] = inv.cantidad_actual);
            globalInventory = prods.map(p => ({
                ...p,
                stock: stkMap[p.ref] ?? 0,
                costo_promedio: Number(p.costo_promedio || 0),
                precio_venta: Number(p.precio_venta || 0)
            }));
        }

    } catch (e) {
        container.innerHTML = '<h2 style="color: #ef4444;">Error cargando módulos de inventario</h2>';
    }
}

function updateVisibility() {
    const table = document.getElementById('tabla-compras');
    const empty = document.getElementById('compras-vacio');
    if (purchaseCart.length > 0) {
        if (table) table.style.display = 'table';
        if (empty) empty.style.display = 'none';
    } else {
        if (table) table.style.display = 'none';
        if (empty) empty.style.display = '';
    }
}