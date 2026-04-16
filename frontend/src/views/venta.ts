import { api } from '../api/endpoints';
import type { Product, Inventory } from '../api/endpoints';

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

function renderCart() {
    const tbody = document.getElementById('tabla-carrito')!;
    const spanTotal = document.getElementById('total-venta')!;
    const btnCharge = document.getElementById('btn-cobrar') as HTMLButtonElement;

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

    spanTotal.textContent = total.toFixed(2);

    // Enable/disable button
    if (btnCharge) {
        btnCharge.disabled = cart.length === 0;
        btnCharge.style.opacity = cart.length === 0 ? '0.5' : '1';
    }
}

export async function renderNewSale(container: HTMLElement) {
    cart = [];
    globalInventory = [];

    container.innerHTML = '<h2 class="loading-state">Cargando productos...</h2>';

    try {
        const [products, inventories]: [Product[], Inventory[]] = await Promise.all([
            api.getProducts(),
            api.getInventories(),
        ]);

        const stockMap: Record<string, number> = {};
        inventories.forEach(inv => {
            stockMap[inv.ref_producto] = inv.cantidad_actual;
        });

        globalInventory = products.map(p => ({
            ref: p.ref,
            nombre: p.nombre,
            precio_venta: Number(p.precio_venta),
            stock: stockMap[p.ref] ?? 0,
        }));

        container.innerHTML = `
            <div class="page-header">
                <h1><i class='bx bx-dollar-circle text-accent mr-6'></i>Registrar Venta</h1>
            </div>

            <!-- SEARCH BAR -->
            <div class="pos-search-wrapper">
                <i class='bx bx-search pos-search-icon'></i>
                <input
                    type="text"
                    id="buscador-productos"
                    placeholder="Buscar producto (ej. Coca Cola)..."
                    autocomplete="off"
                >
                <div id="dropdown-resultados" class="pos-dropdown"></div>
            </div>

            <!-- EMPTY CART OR TABLE -->
            <div id="carrito-vacio" class="pos-empty-state">
                <i class='bx bx-cart empty-icon'></i>
                <p>Agrega productos usando el buscador</p>
            </div>

            <table id="tabla-venta" style="display: none;">
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Precio</th>
                        <th>Cantidad</th>
                        <th>Subtotal</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody id="tabla-carrito"></tbody>
            </table>

            <!-- FOOTER -->
            <div class="pos-footer">
                <div class="pos-total">
                    Total: <span class="pos-total-amount">$<span id="total-venta">0.00</span></span>
                </div>
                <button id="btn-cobrar" class="btn pos-btn-cobrar" disabled style="opacity: 0.5;">
                    <i class='bx bx-check-circle fs-icon-lg'></i>
                    Registrar Venta
                </button>
            </div>

            <!-- FEEDBACK -->
            <div id="venta-feedback" class="pos-feedback" style="display: none;"></div>
        `;

        const searchInput = document.getElementById('buscador-productos') as HTMLInputElement;
        const dropdown = document.getElementById('dropdown-resultados')!;

        searchInput.focus();

        searchInput.addEventListener('input', () => {
            const text = searchInput.value.toLowerCase().trim();

            if (text.length === 0) {
                dropdown.style.display = 'none';
                return;
            }

            const results = globalInventory.filter(p =>
                p.nombre.toLowerCase().includes(text)
            ).slice(0, 10);

            if (results.length > 0) {
                dropdown.innerHTML = results.map(p => {
                    const inCart = cart.find(c => c.ref === p.ref)?.cantidad ?? 0;
                    const availableStock = p.stock - inCart;
                    const outOfStock = availableStock <= 0;

                    return `
                    <div class="pos-dropdown-item ${outOfStock ? 'pos-dropdown-disabled' : ''}" data-id="${p.ref}">
                        <span class="pos-dropdown-name">${p.nombre}</span>
                        <span class="pos-dropdown-meta">
                            <span class="${outOfStock ? 'text-secondary' : 'text-success'}">$${p.precio_venta.toFixed(2)}</span>
                            <span class="pos-dropdown-stock ${outOfStock ? 'text-error' : ''}">
                                ${outOfStock ? 'Sin stock' : `Stock: ${availableStock}`}
                            </span>
                        </span>
                    </div>
                `;
                }).join('');
                dropdown.style.display = 'block';
            } else {
                dropdown.innerHTML = `<div class="pos-dropdown-item pos-dropdown-empty">Nada por aqui</div>`;
                dropdown.style.display = 'block';
            }
        });

        dropdown.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            const itemDiv = target.closest('.pos-dropdown-item') as HTMLElement;

            if (!itemDiv || itemDiv.classList.contains('pos-dropdown-empty') || itemDiv.classList.contains('pos-dropdown-disabled')) return;

            const productId = itemDiv.getAttribute('data-id');
            const product = globalInventory.find(p => p.ref === productId);

            if (product) {
                const inCart = cart.find(item => item.ref === product.ref);
                const currentQuantity = inCart?.cantidad ?? 0;

                if (currentQuantity >= product.stock) return;

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

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const firstItem = dropdown.querySelector('.pos-dropdown-item:not(.pos-dropdown-empty)') as HTMLElement;
                if (firstItem) {
                    firstItem.click();
                }
            }
        });

        document.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            if (!target.closest('.pos-search-wrapper')) {
                dropdown.style.display = 'none';
            }
        });

        document.getElementById('tabla-carrito')!.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            const btn = target.closest('[data-index]') as HTMLElement;
            if (!btn) return;

            const index = parseInt(btn.getAttribute('data-index') || '-1');
            if (index === -1) return;

            if (btn.classList.contains('btn-sumar')) {
                const prod = globalInventory.find(p => p.ref === cart[index].ref);
                if (prod && cart[index].cantidad >= prod.stock) return;
                cart[index].cantidad += 1;
            } else if (btn.classList.contains('btn-restar')) {
                cart[index].cantidad -= 1;
                if (cart[index].cantidad <= 0) {
                    cart.splice(index, 1);
                }
            } else if (btn.classList.contains('btn-eliminar-carrito')) {
                cart.splice(index, 1);
            }

            updateTable();
            renderCart();
            searchInput.focus();
        });

        document.getElementById('btn-cobrar')!.addEventListener('click', async () => {
            if (cart.length === 0) return;

            const btnCharge = document.getElementById('btn-cobrar') as HTMLButtonElement;
            const feedback = document.getElementById('venta-feedback')!;

            btnCharge.disabled = true;
            btnCharge.innerHTML = `<i class='bx bx-loader-alt bx-spin fs-icon-lg'></i> Procesando...`;

            try {
                const items = cart.map(item => ({
                    ref_producto: item.ref,
                    cantidad: item.cantidad,
                    precio_unitario: item.precio,
                }));

                const result: any = await api.registerQuickSale(items);

                cart = [];
                updateTable();
                renderCart();

                const newInventories = await api.getInventories();
                const newStock: Record<string, number> = {};
                newInventories.forEach(inv => {
                    newStock[inv.ref_producto] = inv.cantidad_actual;
                });
                globalInventory.forEach(p => {
                    p.stock = newStock[p.ref] ?? 0;
                });

                feedback.className = 'pos-feedback pos-feedback-success';
                feedback.innerHTML = `<i class='bx bx-check-circle'></i> ${result.mensaje} — Total: $${result.venta?.total?.toFixed(2) ?? '0.00'}`;
                feedback.style.display = 'flex';

                setTimeout(() => {
                    feedback.style.display = 'none';
                }, 4000);

                searchInput.focus();
            } catch (err: any) {
                feedback.className = 'pos-feedback pos-feedback-error';
                feedback.innerHTML = `<i class='bx bx-error-circle'></i> ${err.message || 'Error al registrar venta'}`;
                feedback.style.display = 'flex';

                setTimeout(() => {
                    feedback.style.display = 'none';
                }, 5000);
            } finally {
                btnCharge.disabled = cart.length === 0;
                btnCharge.style.opacity = cart.length === 0 ? '0.5' : '1';
                btnCharge.innerHTML = `<i class='bx bx-check-circle fs-icon-lg'></i> Registrar Venta`;
            }
        });

    } catch (error) {
        container.innerHTML = '<h2 class="error-state">Error cargando productos</h2><p class="error-hint">Verifica que el backend esté corriendo.</p>';
    }
}

function updateTable() {
    const table = document.getElementById('tabla-venta');
    const empty = document.getElementById('carrito-vacio');

    if (cart.length > 0) {
        if (table) table.style.display = '';
        if (empty) empty.style.display = 'none';
    } else {
        if (table) table.style.display = 'none';
        if (empty) empty.style.display = '';
    }
}
