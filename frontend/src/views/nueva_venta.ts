import { api } from '../api/endpoints';
import type { Producto, Inventario } from '../api/endpoints';
// AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
interface ProductoConStock {
    ref: string;
    nombre: string;
    precio_venta: number;
    stock: number;
}

interface ItemCarrito {
    ref: string;
    nombre: string;
    precio: number;
    cantidad: number;
}

let inventarioGlobal: ProductoConStock[] = [];
let carrito: ItemCarrito[] = [];

function renderizarCarrito() {
    const tbody = document.getElementById('tabla-carrito')!;
    const spanTotal = document.getElementById('total-venta')!;
    const btnCobrar = document.getElementById('btn-cobrar') as HTMLButtonElement;

    let total = 0;

    tbody.innerHTML = carrito.map((item, index) => {
        const subtotal = item.precio * item.cantidad;
        total += subtotal;

        return `
            <tr>
                <td style="font-weight: 500; color: #f3f4f6;">${item.nombre}</td>
                <td>$${Number(item.precio).toFixed(2)}</td>
                <td>
                    <div class="qty-controls">
                        <button class="btn-qty btn-restar" data-index="${index}">−</button>
                        <span class="qty-value">${item.cantidad}</span>
                        <button class="btn-qty btn-sumar" data-index="${index}">+</button>
                    </div>
                </td>
                <td style="color: #10b981; font-weight: 600;">$${subtotal.toFixed(2)}</td>
                <td>
                    <button class="btn btn-danger btn-sm btn-eliminar-carrito" data-index="${index}">
                        <i class='bx bx-x' style="font-size: 1rem;"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');

    spanTotal.textContent = total.toFixed(2);

    // Habilitar/deshabilitar botón, que hueva
    if (btnCobrar) {
        btnCobrar.disabled = carrito.length === 0;
        btnCobrar.style.opacity = carrito.length === 0 ? '0.5' : '1';
    }
}

export async function renderNuevaVenta(container: HTMLElement) {
    carrito = [];
    inventarioGlobal = [];

    container.innerHTML = '<h2 style="color: #4b5563; padding-top: 40px;">Cargando productos...</h2>';

    try {
        const [productos, inventarios]: [Producto[], Inventario[]] = await Promise.all([
            api.getProductos(),
            api.getInventarios(),
        ]);

        const stockMap: Record<string, number> = {};
        inventarios.forEach(inv => {
            stockMap[inv.ref_producto] = inv.cantidad_actual;
        });

        inventarioGlobal = productos.map(p => ({
            ref: p.ref,
            nombre: p.nombre,
            precio_venta: Number(p.precio_venta),
            stock: stockMap[p.ref] ?? 0,
        }));

        container.innerHTML = `
            <div class="page-header">
                <h1><i class='bx bx-dollar-circle' style="color: #6366f1; margin-right: 6px;"></i>Registrar Venta</h1>
            </div>

            <!-- BUSCADOR -->
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

            <!-- CARRITO VACÍO / TABLA -->
            <div id="carrito-vacio" class="pos-empty-state">
                <i class='bx bx-cart' style="font-size: 3rem; color: #2a2a2e;"></i>
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
                    <i class='bx bx-check-circle' style="font-size: 1.3rem;"></i>
                    Registrar Venta
                </button>
            </div>

            <!-- FEEDBACK -->
            <div id="venta-feedback" class="pos-feedback" style="display: none;"></div>
        `;
        // Asi se ven 10 años de seniorio en UX, :v.
        const inputBuscador = document.getElementById('buscador-productos') as HTMLInputElement;
        const dropdown = document.getElementById('dropdown-resultados')!;

        inputBuscador.focus();

        inputBuscador.addEventListener('input', () => {
            const texto = inputBuscador.value.toLowerCase().trim();

            if (texto.length === 0) {
                dropdown.style.display = 'none';
                return;
            }

            const resultados = inventarioGlobal.filter(p =>
                p.nombre.toLowerCase().includes(texto)
            ).slice(0, 10);

            if (resultados.length > 0) {
                dropdown.innerHTML = resultados.map(p => {
                    const enCarrito = carrito.find(c => c.ref === p.ref)?.cantidad ?? 0;
                    const stockDisponible = p.stock - enCarrito;
                    const sinStock = stockDisponible <= 0;

                    return `
                    <div class="pos-dropdown-item ${sinStock ? 'pos-dropdown-disabled' : ''}" data-id="${p.ref}">
                        <span class="pos-dropdown-name">${p.nombre}</span>
                        <span class="pos-dropdown-meta">
                            <span style="color: ${sinStock ? '#6b7280' : '#10b981'};">$${p.precio_venta.toFixed(2)}</span>
                            <span class="pos-dropdown-stock" style="color: ${sinStock ? '#ef4444' : '#6b7280'};">
                                ${sinStock ? 'Sin stock' : `Stock: ${stockDisponible}`}
                            </span>
                        </span>
                    </div>
                `;
                }).join('');
                dropdown.style.display = 'block';
            } else {
                dropdown.innerHTML = `<div class="pos-dropdown-item pos-dropdown-empty">No se encontraron productos</div>`;
                dropdown.style.display = 'block';
            }
        });

        dropdown.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            const itemDiv = target.closest('.pos-dropdown-item') as HTMLElement;

            if (!itemDiv || itemDiv.classList.contains('pos-dropdown-empty') || itemDiv.classList.contains('pos-dropdown-disabled')) return;

            const idProducto = itemDiv.getAttribute('data-id');
            const producto = inventarioGlobal.find(p => p.ref === idProducto);

            if (producto) {
                const enCarrito = carrito.find(item => item.ref === producto.ref);
                const cantidadActual = enCarrito?.cantidad ?? 0;

                if (cantidadActual >= producto.stock) return;

                if (enCarrito) {
                    enCarrito.cantidad += 1;
                } else {
                    carrito.push({
                        ref: producto.ref,
                        nombre: producto.nombre,
                        precio: producto.precio_venta,
                        cantidad: 1,
                    });
                }

                inputBuscador.value = '';
                dropdown.style.display = 'none';
                inputBuscador.focus();

                actualizarVisibilidadTabla();
                renderizarCarrito();
            }
        });

        inputBuscador.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const primerItem = dropdown.querySelector('.pos-dropdown-item:not(.pos-dropdown-empty)') as HTMLElement;
                if (primerItem) {
                    primerItem.click();
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
                const prod = inventarioGlobal.find(p => p.ref === carrito[index].ref);
                if (prod && carrito[index].cantidad >= prod.stock) return;
                carrito[index].cantidad += 1;
            } else if (btn.classList.contains('btn-restar')) {
                carrito[index].cantidad -= 1;
                if (carrito[index].cantidad <= 0) {
                    carrito.splice(index, 1);
                }
            } else if (btn.classList.contains('btn-eliminar-carrito')) {
                carrito.splice(index, 1);
            }

            actualizarVisibilidadTabla();
            renderizarCarrito();
            inputBuscador.focus();
        });

        document.getElementById('btn-cobrar')!.addEventListener('click', async () => {
            if (carrito.length === 0) return;

            const btnCobrar = document.getElementById('btn-cobrar') as HTMLButtonElement;
            const feedback = document.getElementById('venta-feedback')!;

            btnCobrar.disabled = true;
            btnCobrar.innerHTML = `<i class='bx bx-loader-alt bx-spin' style="font-size: 1.3rem;"></i> Procesando...`;

            try {
                const items = carrito.map(item => ({
                    ref_producto: item.ref,
                    cantidad: item.cantidad,
                    precio_unitario: item.precio,
                }));

                const result: any = await api.registrarVentaRapida(items);

                carrito = [];
                actualizarVisibilidadTabla();
                renderizarCarrito();

                const nuevosInv = await api.getInventarios();
                const nuevoStock: Record<string, number> = {};
                nuevosInv.forEach(inv => {
                    nuevoStock[inv.ref_producto] = inv.cantidad_actual;
                });
                inventarioGlobal.forEach(p => {
                    p.stock = nuevoStock[p.ref] ?? 0;
                });

                feedback.className = 'pos-feedback pos-feedback-success';
                feedback.innerHTML = `<i class='bx bx-check-circle'></i> ${result.mensaje} — Total: $${result.venta?.total?.toFixed(2) ?? '0.00'}`;
                feedback.style.display = 'flex';

                setTimeout(() => {
                    feedback.style.display = 'none';
                }, 4000);

                inputBuscador.focus();
            } catch (err: any) {
                feedback.className = 'pos-feedback pos-feedback-error';
                feedback.innerHTML = `<i class='bx bx-error-circle'></i> ${err.message || 'Error al registrar venta'}`;
                feedback.style.display = 'flex';

                setTimeout(() => {
                    feedback.style.display = 'none';
                }, 5000);
            } finally {
                btnCobrar.disabled = carrito.length === 0;
                btnCobrar.style.opacity = carrito.length === 0 ? '0.5' : '1';
                btnCobrar.innerHTML = `<i class='bx bx-check-circle' style="font-size: 1.3rem;"></i> Registrar Venta`;
            }
        });

    } catch (error) {
        container.innerHTML = '<h2 style="color: #ef4444;">Error cargando productos</h2><p style="color: #9ca3af;">Verifica que el backend esté corriendo.</p>';
    }
}

function actualizarVisibilidadTabla() {
    const tabla = document.getElementById('tabla-venta');
    const vacio = document.getElementById('carrito-vacio');

    if (carrito.length > 0) {
        if (tabla) tabla.style.display = '';
        if (vacio) vacio.style.display = 'none';
    } else {
        if (tabla) tabla.style.display = 'none';
        if (vacio) vacio.style.display = '';
    }
}
