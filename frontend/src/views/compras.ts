import { api } from '../api/endpoints';
import type { Producto, Categoria } from '../api/endpoints';

interface ProductoCompraInfo {
    ref?: string;
    nombre: string;
    costo: number;
    precio_venta: number;
    cantidad: number;
    ref_categoria?: string;
    solo_stock: boolean;
}

let inventarioGlobal: (Producto & { stock: number })[] = [];
let categoriasGlobal: Categoria[] = [];
let carritoCompras: ProductoCompraInfo[] = [];

function renderComprasCarrito() {
    const tbody = document.getElementById('tabla-compras-carrito')!;
    const spanTotal = document.getElementById('total-compra')!;
    const btnRegistrar = document.getElementById('btn-registrar-compra') as HTMLButtonElement;

    let total = 0;

    tbody.innerHTML = carritoCompras.map((item, index) => {
        if (!item.solo_stock) {
            total += item.costo * item.cantidad;
        }

        const catOptions = categoriasGlobal.map(c =>
            `<option value="${c.ref}" ${c.ref === item.ref_categoria ? 'selected' : ''}>${c.nombre}</option>`
        ).join('');

        const esNuevo = !item.ref;

        return `
            <tr class="compra-row ${item.solo_stock ? 'compra-row--solo-stock' : ''}">
                <td>
                    <div style="display:flex;align-items:center;gap:6px;">
                        ${esNuevo ? '<span style="background:#6366f1;color:#fff;font-size:0.6rem;padding:1px 5px;border-radius:4px;font-weight:600;">NUEVO</span>' : ''}
                        <input type="text" class="pos-input-edit compra-input" data-field="nombre" data-index="${index}" value="${item.nombre}" placeholder="Nombre del producto" />
                    </div>
                </td>
                <td>
                    <select class="pos-input-edit compra-select" data-field="ref_categoria" data-index="${index}">
                        <option value="">—</option>
                        ${catOptions}
                    </select>
                </td>
                <td>
                    <div class="compra-price-cell">
                        <span class="compra-dollar">$</span>
                        <input type="number" step="0.01" min="0" class="pos-input-edit compra-input compra-input--num" data-field="costo" data-index="${index}" value="${item.costo}" ${item.solo_stock ? 'disabled' : ''} />
                    </div>
                </td>
                <td>
                    <div class="compra-price-cell">
                        <span class="compra-dollar">$</span>
                        <input type="number" step="0.01" min="0" class="pos-input-edit compra-input compra-input--num" data-field="precio_venta" data-index="${index}" value="${item.precio_venta}" />
                    </div>
                </td>
                <td>
                    <input type="number" min="1" step="1" class="pos-input-edit compra-input compra-input--qty" data-field="cantidad" data-index="${index}" value="${item.cantidad}" />
                </td>
                <td style="text-align:center;">
                    <label class="compra-checkbox-label">
                        <input type="checkbox" class="pos-input-checkbox" data-index="${index}" ${item.solo_stock ? 'checked' : ''} />
                        <span>Solo stock</span>
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

    if (btnRegistrar) {
        btnRegistrar.disabled = carritoCompras.length === 0;
        btnRegistrar.style.opacity = carritoCompras.length === 0 ? '0.5' : '1';
    }
}

function tieneDuplicados(): string | null {
    const nombres = carritoCompras.map(c => c.nombre.trim().toLowerCase());
    const visto = new Set<string>();
    for (const n of nombres) {
        if (visto.has(n)) return n;
        visto.add(n);
    }
    return null;
}

function agregarProductoExistente(producto: Producto & { stock: number }) {
    const yaEsta = carritoCompras.find(c => c.ref === producto.ref);
    if (!yaEsta) {
        carritoCompras.push({
            ref: producto.ref,
            nombre: producto.nombre,
            costo: Number(producto.costo_promedio),
            precio_venta: Number(producto.precio_venta),
            ref_categoria: producto.ref_categoria,
            cantidad: 1,
            solo_stock: false
        });
    } else {
        yaEsta.cantidad += 1;
    }
}

function agregarProductoNuevo(nombreBase: string) {
    const existe = carritoCompras.some(c => c.nombre.trim().toLowerCase() === nombreBase.trim().toLowerCase());
    if (existe) return;

    carritoCompras.push({
        nombre: nombreBase || 'Nuevo Producto',
        costo: 0,
        precio_venta: 0,
        cantidad: 1,
        solo_stock: false
    });
}

export async function renderCompras(container: HTMLElement) {
    carritoCompras = [];
    inventarioGlobal = [];
    categoriasGlobal = [];

    container.innerHTML = '<h2 style="color: #4b5563; padding-top: 40px;">Cargando inventario...</h2>';

    try {
        const [productos, inventarios, categorias] = await Promise.all([
            api.getProductos(),
            api.getInventarios(),
            api.getCategorias(),
        ]);

        categoriasGlobal = categorias;
        const stockMap: Record<string, number> = {};
        inventarios.forEach(inv => stockMap[inv.ref_producto] = inv.cantidad_actual);

        inventarioGlobal = productos.map(p => ({
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
                <table id="tabla-compras" class="compra-table" style="display: none;">
                    <thead>
                        <tr>
                            <th style="width:26%;">Producto</th>
                            <th style="width:14%;">Categoría</th>
                            <th style="width:12%;">Costo Un.</th>
                            <th style="width:12%;">P. Venta</th>
                            <th style="width:10%;">Cant.</th>
                            <th style="width:13%;">Opción</th>
                            <th style="width:50px;"></th>
                        </tr>
                    </thead>
                    <tbody id="tabla-compras-carrito"></tbody>
                </table>
            </div>

            <div class="pos-footer" style="padding: 15px 0;">
                <div class="pos-total">
                    Total Inversión: <span class="pos-total-amount" style="color: #10b981;">$<span id="total-compra">0.00</span></span>
                </div>
                <button id="btn-registrar-compra" class="btn pos-btn-cobrar" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" disabled>
                    <i class='bx bx-save' style="font-size: 1.3rem;"></i>
                    Registrar Compra
                </button>
            </div>

            <div id="compra-feedback" class="pos-feedback" style="display: none;"></div>
        `;

        const inputBuscador = document.getElementById('buscador-compras') as HTMLInputElement;
        const dropdown = document.getElementById('dropdown-compras')!;
        inputBuscador.focus();

        inputBuscador.addEventListener('input', () => {
            const texto = inputBuscador.value.toLowerCase().trim();
            if (!texto) { dropdown.style.display = 'none'; return; }

            const resultados = inventarioGlobal.filter(p => p.nombre.toLowerCase().includes(texto)).slice(0, 10);

            if (resultados.length > 0) {
                dropdown.innerHTML = resultados.map(p => `
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

            const idProducto = itemDiv.getAttribute('data-id');
            const producto = inventarioGlobal.find(p => p.ref === idProducto);

            if (producto) {
                agregarProductoExistente(producto);
                inputBuscador.value = '';
                dropdown.style.display = 'none';
                inputBuscador.focus();
                actualizarVisibilidad();
                renderComprasCarrito();
            }
        });

        inputBuscador.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const texto = inputBuscador.value.trim();
                if (!texto) return;

                if (e.shiftKey) {
                    const existeEnCarrito = carritoCompras.some(c => c.nombre.trim().toLowerCase() === texto.toLowerCase());
                    const existeEnInventario = inventarioGlobal.some(p => p.nombre.trim().toLowerCase() === texto.toLowerCase());
                    if (existeEnCarrito || existeEnInventario) {
                        mostrarFeedback('error', `Ya existe un producto con el nombre "${texto}"`);
                        return;
                    }
                    agregarProductoNuevo(texto);
                } else {
                    const primerItem = dropdown.querySelector('.pos-dropdown-item:not(.pos-dropdown-empty)') as HTMLElement;
                    if (primerItem) {
                        primerItem.click();
                        return;
                    }
                }

                inputBuscador.value = '';
                dropdown.style.display = 'none';
                inputBuscador.focus();
                actualizarVisibilidad();
                renderComprasCarrito();
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
                const field = target.getAttribute('data-field') as keyof ProductoCompraInfo;
                if (field === 'cantidad' || field === 'costo' || field === 'precio_venta') {
                    (carritoCompras[i] as any)[field] = parseFloat(target.value) || 0;
                } else if (field === 'nombre') {
                    const nuevoNombre = target.value.trim().toLowerCase();
                    const dupEnCarrito = carritoCompras.some((c, ci) => ci !== i && c.nombre.trim().toLowerCase() === nuevoNombre);
                    const dupEnInventario = inventarioGlobal.some(p =>
                        p.ref !== carritoCompras[i].ref && p.nombre.trim().toLowerCase() === nuevoNombre
                    );
                    if (dupEnCarrito || dupEnInventario) {
                        mostrarFeedback('error', `Ya existe un producto con ese nombre`);
                        target.value = carritoCompras[i].nombre;
                        return;
                    }
                    carritoCompras[i].nombre = target.value;
                } else {
                    (carritoCompras[i] as any)[field] = target.value;
                }
                renderComprasCarrito();
            } else if (target.classList.contains('pos-input-checkbox')) {
                carritoCompras[i].solo_stock = (target as HTMLInputElement).checked;
                renderComprasCarrito();
            }
        });

        document.getElementById('tabla-compras')!.addEventListener('click', (e) => {
            const target = e.target as HTMLElement;
            const btn = target.closest('.btn-eliminar-compra');
            if (btn) {
                const index = parseInt(btn.getAttribute('data-index') || '0');
                carritoCompras.splice(index, 1);
                actualizarVisibilidad();
                renderComprasCarrito();
            }
        });

        document.getElementById('btn-registrar-compra')!.addEventListener('click', async () => {
            if (carritoCompras.length === 0) return;

            const dup = tieneDuplicados();
            if (dup) {
                mostrarFeedback('error', `Hay nombres duplicados en la lista: "${dup}"`);
                return;
            }

            const btnReg = document.getElementById('btn-registrar-compra') as HTMLButtonElement;

            btnReg.disabled = true;
            btnReg.innerHTML = `<i class='bx bx-loader-alt bx-spin'></i> Procesando...`;

            try {
                const payload = carritoCompras.map(c => ({
                    ref_producto: c.ref || null,
                    nombre: c.nombre,
                    costo: c.costo,
                    precio_venta: c.precio_venta,
                    ref_categoria: c.ref_categoria,
                    cantidad: c.cantidad,
                    solo_stock: c.solo_stock
                }));

                const result: any = await api.registrarCompraRapida(payload);

                carritoCompras = [];
                actualizarVisibilidad();
                renderComprasCarrito();

                await reloadInventarioSilent();

                mostrarFeedback('success', `${result.mensaje} — Total: $${(result.compra?.total ?? 0).toFixed(2)}`);

            } catch (err: any) {
                mostrarFeedback('error', err.message || 'Error al registrar');
            } finally {
                btnReg.disabled = carritoCompras.length === 0;
                btnReg.style.opacity = carritoCompras.length === 0 ? '0.5' : '1';
                btnReg.innerHTML = `<i class='bx bx-save' style="font-size: 1.3rem;"></i> Registrar Compra`;
            }
        });

        function mostrarFeedback(tipo: 'success' | 'error', msg: string) {
            const feedback = document.getElementById('compra-feedback')!;
            feedback.className = `pos-feedback pos-feedback-${tipo}`;
            const icon = tipo === 'success' ? 'bx-check-circle' : 'bx-error-circle';
            feedback.innerHTML = `<i class='bx ${icon}'></i> ${msg}`;
            feedback.style.display = 'flex';
            setTimeout(() => feedback.style.display = 'none', 5000);
        }

        async function reloadInventarioSilent() {
            const [prods, invs] = await Promise.all([api.getProductos(), api.getInventarios()]);
            const stkMap: Record<string, number> = {};
            invs.forEach(inv => stkMap[inv.ref_producto] = inv.cantidad_actual);
            inventarioGlobal = prods.map(p => ({
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

function actualizarVisibilidad() {
    const tabla = document.getElementById('tabla-compras');
    const vacio = document.getElementById('compras-vacio');
    if (carritoCompras.length > 0) {
        if (tabla) tabla.style.display = 'table';
        if (vacio) vacio.style.display = 'none';
    } else {
        if (tabla) tabla.style.display = 'none';
        if (vacio) vacio.style.display = '';
    }
}
