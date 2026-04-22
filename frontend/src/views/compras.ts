import { api } from '../api/endpoints';
import type { Product, Category } from '../api/endpoints';

// ———— Interfaces ————

interface PurchaseProductInfo {
    ref?: string;
    nombre: string;
    costo: number;
    precio_venta: number;
    cantidad: number;
    ref_categoria?: string;
}

// ———— Global State ————

let globalInventory: (Product & { stock: number })[] = [];
let globalCategories: Category[] = [];
let purchaseCart: PurchaseProductInfo[] = [];

// ———— Render Functions ————

function renderPurchaseCart() {
    const tbody = document.getElementById('tabla-compras-carrito')!;
    const spanTotal = document.getElementById('total-compra')!;
    const btnRegister = document.getElementById('btn-registrar-compra') as HTMLButtonElement;
    let total = 0;

    tbody.innerHTML = purchaseCart.map((item, index) => {
        total += item.costo * item.cantidad;

        const categoryOptions = globalCategories.map(c =>
            `<option value="${c.ref}" ${c.ref === item.ref_categoria ? 'selected' : ''}>${c.nombre}</option>`
        ).join('');

        const isNew = !item.ref;

        return `
            <tr class="compra-row">
                <td>
                    <div class="compra-cell-flex">
                        ${isNew ? '<span class="compra-badge-new">NUEVO</span>' : ''}
                        <input type="text" class="pos-input-edit compra-input" data-field="nombre" data-index="${index}" value="${item.nombre}" placeholder="Nombre del producto" />
                    </div>
                </td>
                <td>
                    <select class="pos-input-edit compra-select" data-field="ref_categoria" data-index="${index}">
                        <option value="">—</option>
                        ${categoryOptions}
                    </select>
                </td>
                <td>
                    <div class="compra-price-cell">
                        <span class="compra-dollar">$</span>
                        <input type="number" step="0.01" min="0" class="pos-input-edit compra-input compra-input--num" data-field="costo" data-index="${index}" value="${item.costo}" />
                        <div class="compra-spin-wrapper">
                            <button type="button" class="compra-spin-btn compra-spin-btn--up" data-field="costo" data-index="${index}">▲</button>
                            <button type="button" class="compra-spin-btn compra-spin-btn--down" data-field="costo" data-index="${index}">▼</button>
                        </div>
                    </div>
                </td>
                <td>
                    <div class="compra-price-cell">
                        <span class="compra-dollar">$</span>
                        <input type="number" step="0.01" min="0" class="pos-input-edit compra-input compra-input--num" data-field="precio_venta" data-index="${index}" value="${item.precio_venta}" />
                        <div class="compra-spin-wrapper">
                            <button type="button" class="compra-spin-btn compra-spin-btn--up" data-field="precio_venta" data-index="${index}">▲</button>
                            <button type="button" class="compra-spin-btn compra-spin-btn--down" data-field="precio_venta" data-index="${index}">▼</button>
                        </div>
                    </div>
                </td>
                <td>
                    <div class="qty-controls">
                        <button class="btn-qty btn-restar-compra" data-index="${index}">−</button>
                        <input type="number" min="1" step="1" class="qty-value-input compra-input" data-field="cantidad" data-index="${index}" value="${item.cantidad}" />
                        <button class="btn-qty btn-sumar-compra" data-index="${index}">+</button>
                    </div>
                </td>
                <td class="text-center">
                    <button class="btn btn-danger btn-sm btn-eliminar-compra" data-index="${index}" title="Quitar">
                        <i class='bx bx-x fs-icon'></i>
                    </button>
                </td>
            </tr>`;
    }).join('');

    spanTotal.textContent = total.toFixed(2);

    if (btnRegister) {
        btnRegister.disabled = purchaseCart.length === 0;
        btnRegister.style.opacity = purchaseCart.length === 0 ? '0.5' : '1';
    }
}

// ———— Utility Functions ————

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
            cantidad: 1
        });
    } else {
        alreadyExists.cantidad += 1;
    }
}

function addNewProduct(baseName: string) {
    if (purchaseCart.some(c => c.nombre.trim().toLowerCase() === baseName.trim().toLowerCase())) return;
    purchaseCart.push({
        nombre: baseName || 'Nuevo Producto',
        costo: 0,
        precio_venta: 0,
        cantidad: 1
    });
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

// ———— Main Export ————

export async function renderPurchases(container: HTMLElement) {
    purchaseCart = [];
    globalInventory = [];
    globalCategories = [];

    container.innerHTML = '<h2 class="loading-state">Cargando inventario...</h2>';

    try {
        const [products, inventories, categories] = await Promise.all([
            api.getProducts(),
            api.getInventories(),
            api.getCategories()
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
                <h1><i class='bx bx-archive-in text-success mr-8'></i>Registrar Compra</h1>
                <div class="header-actions">
                    <input type="datetime-local" id="compra-fecha" class="pos-input-edit" title="Fecha de la compra" />
                </div>
            </div>
            
            <div class="pos-search-wrapper pos-search-wrapper--compact">
                <i class='bx bx-search pos-search-icon'></i>
                <input type="text" id="buscador-compras" placeholder="Buscar producto existente (Enter) · Crear nuevo (Shift + Enter)" autocomplete="off">
                <div id="dropdown-compras" class="pos-dropdown"></div>
            </div>
            
            <div id="compras-vacio" class="pos-empty-state">
                <i class='bx bx-box empty-icon-sm'></i>
                <p class="pos-hint">Busca un producto y presiona <kbd>Enter</kbd> para agregarlo</p>
                <small class="pos-hint-sub">o <kbd class="kbd-sm">Shift + Enter</kbd> para crear uno nuevo con ese nombre</small>
            </div>
            
            <div class="compra-table-wrapper">
                <table id="tabla-compras" class="compra-table" style="display: none;">
                    <thead>
                        <tr>
                            <th class="col-producto">Producto</th>
                            <th class="col-categoria">Categoría</th>
                            <th class="col-costo">Costo Un.</th>
                            <th class="col-pventa">P. Venta</th>
                            <th class="col-cantidad">Cant.</th>
                            <th class="col-accion"></th>
                        </tr>
                    </thead>
                    <tbody id="tabla-compras-carrito"></tbody>
                </table>
            </div>
            
            <div class="pos-footer">
                <div class="pos-total">Total Inversión: <span class="pos-total-amount">$<span id="total-compra">0.00</span></span></div>
                <button id="btn-registrar-compra" class="btn pos-btn-cobrar pos-btn-registrar" disabled>
                    <i class='bx bx-save fs-icon'></i> Registrar Compra
                </button>
            </div>
            
            <div id="compra-feedback" class="pos-feedback" style="display: none;"></div>
        `;

        // ———— Date Initialization ————

        const dateInput = document.getElementById('compra-fecha') as HTMLInputElement;
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        dateInput.value = now.toISOString().slice(0, 16);

        // ———— DOM Elements & Events ————

        const searchInput = document.getElementById('buscador-compras') as HTMLInputElement;
        const dropdown = document.getElementById('dropdown-compras')!;
        searchInput.focus();

        searchInput.addEventListener('input', () => {
            const text = searchInput.value.toLowerCase().trim();
            if (!text) {
                dropdown.style.display = 'none';
                return;
            }

            const results = globalInventory.filter(p => p.nombre.toLowerCase().includes(text)).slice(0, 10);

            if (results.length > 0) {
                dropdown.innerHTML = results.map(p => `
                    <div class="pos-dropdown-item" data-id="${p.ref}">
                        <span class="pos-dropdown-name">${p.nombre}</span>
                        <span class="pos-dropdown-meta">
                            <span class="text-secondary">Stock: ${p.stock}</span>
                            <span class="text-success">CPP: $${Number(p.costo_promedio).toFixed(2)}</span>
                        </span>
                    </div>`).join('');
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

            const product = globalInventory.find(p => p.ref === itemDiv.getAttribute('data-id'));
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
            if (!(e.target as HTMLElement).closest('.pos-search-wrapper')) {
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
                    const dupInInventory = globalInventory.some(p => p.ref !== purchaseCart[i].ref && p.nombre.trim().toLowerCase() === newName);

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
            }
        });

        document.getElementById('tabla-compras')!.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;

            const btnEliminar = target.closest('.btn-eliminar-compra');
            if (btnEliminar) {
                purchaseCart.splice(parseInt(btnEliminar.getAttribute('data-index') || '0'), 1);
                updateVisibility();
                renderPurchaseCart();
                return;
            }

            const btnQty = target.closest('.btn-qty');
            if (btnQty) {
                const index = parseInt(btnQty.getAttribute('data-index') || '0');
                if (btnQty.classList.contains('btn-sumar-compra')) {
                    purchaseCart[index].cantidad += 1;
                } else if (btnQty.classList.contains('btn-restar-compra')) {
                    if (purchaseCart[index].cantidad > 1) {
                        purchaseCart[index].cantidad -= 1;
                    }
                }
                renderPurchaseCart();
            }

            const spinBtn = target.closest('.compra-spin-btn') as HTMLElement;
            if (spinBtn) {
                const index = parseInt(spinBtn.getAttribute('data-index') || '0');
                const field = spinBtn.getAttribute('data-field') as 'costo' | 'precio_venta';
                const step = 0.01;
                if (spinBtn.classList.contains('compra-spin-btn--up')) {
                    purchaseCart[index][field] = Math.round((purchaseCart[index][field] + step) * 100) / 100;
                } else {
                    purchaseCart[index][field] = Math.max(0, Math.round((purchaseCart[index][field] - step) * 100) / 100);
                }
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
                const fechaSeleccionada = (document.getElementById('compra-fecha') as HTMLInputElement).value;

                const itemsPayload = purchaseCart.map(c => ({
                    ref_producto: c.ref || null,
                    nombre: c.nombre,
                    costo: c.costo,
                    precio_venta: c.precio_venta,
                    ref_categoria: c.ref_categoria,
                    cantidad: c.cantidad
                }));

                const requestData = {
                    fecha: fechaSeleccionada,
                    items: itemsPayload
                };

                const result: any = await api.registerQuickPurchase(requestData);

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
                btnReg.innerHTML = `<i class='bx bx-save fs-icon'></i> Registrar Compra`;
            }
        });

        function showFeedback(type: 'success' | 'error', msg: string) {
            const feedback = document.getElementById('compra-feedback')!;
            feedback.className = `pos-feedback pos-feedback-${type}`;
            feedback.innerHTML = `<i class='bx ${type === 'success' ? 'bx-check-circle' : 'bx-error-circle'}'></i> ${msg}`;
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
        container.innerHTML = '<h2 class="error-state">Error cargando módulos de inventario</h2>';
    }
}