import { api } from '../api/endpoints';

function precioBadge(precio: number | string): string {
    return `<span style="font-weight: 600;">$${Number(precio).toFixed(2)}</span>`;
}


export async function renderInventario(container: HTMLElement) {
    container.innerHTML = '<h2 style="color: #4b5563; padding-top: 40px;">Cargando inventario...</h2>';

    try {
        // Cargar productos, categorías e inventarios en paralelo
        const [productos, categorias, inventarios] = await Promise.all([
            api.getProductos(),
            api.getCategorias(),
            api.getInventarios(),
        ]);

        const cantPorProd: Record<string, number> = {};
        inventarios.forEach(inv => {
            cantPorProd[inv.ref_producto] = inv.cantidad_actual;
        });


        const filasHTML = productos.map(p => `
            <tr>
                <td style="color: #6b7280; font-weight: 500; font-size: 0.75rem;" title="${p.ref}">${p.ref.slice(0, 8)}…</td>
                <td style="font-weight: 500; color: #f3f4f6;">${p.nombre}</td>
                <td>${precioBadge(p.precio_venta)}</td>
                <td style="color: #9ca3af;">$${Number(p.costo_promedio).toFixed(2)}</td>
                <td style="color: #9ca3af;">${p.unidad_medida}</td>
                <td style="font-weight: bold; color: #10b981;">${cantPorProd[p.ref] ?? 0}</td>
                <td>
                    <button class="btn btn-warning btn-sm btn-edit"
                        data-uuid="${p.ref}"
                        data-nombre="${p.nombre}"
                        data-precio-venta="${p.precio_venta}"
                        data-precio-compra="${p.costo_promedio}"
                        data-unidad="${p.unidad_medida}"
                        data-categoria="${p.ref_categoria}">Editar</button>
                    <button class="btn btn-danger btn-sm btn-delete" data-uuid="${p.ref}" style="margin-left: 6px;">Eliminar</button>
                </td>
            </tr>
        `).join('');

        const categoriasOptions = categorias.map(c =>
            `<option value="${c.ref}">${c.nombre}</option>`
        ).join('');

        container.innerHTML = `
            <div class="page-header">
                <h1>Inventario</h1>
                <button class="btn btn-success" id="btn-add-product">+ Nuevo Producto</button>
            </div>
            <div class="search-bar">
                <input type="search" id="search-input" placeholder="Buscar producto...">
            </div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Precio Venta</th>
                        <th>Precio Compra</th>
                        <th>Unidad</th>
                        <th>Stock</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody id="productos-tbody">
                    ${filasHTML}
                </tbody>
            </table>
            
            <!-- Modal nativo (Dialog) para crear/editar productos -->
            <dialog id="product-modal">
                <h2 id="modal-title">Nuevo Producto</h2>
                <form id="product-form">
                    <input type="hidden" id="product-uuid">
                    <input type="text" id="product-nombre" placeholder="Nombre del producto" required>
                    <input type="number" id="product-precio-venta" placeholder="Precio de venta" step="0.01" min="0" required>
                    <input type="number" id="product-precio-compra" placeholder="Precio de compra" step="0.01" min="0" required>
                    <input type="text" id="product-unidad" placeholder="Unidad de medida (ej: unidad, kg)" required>
                    <div id="container-cantidad-actual" style="margin-bottom: var(--spacing, 0); width: 100%;">
                        <input type="number" id="product-cantidad-actual" placeholder="Cantidad actual en inventario" step="1" min="0" required style="width: 100%; box-sizing: border-box;">
                    </div>
                    <select id="product-categoria" required>
                        <option value="" disabled selected>Seleccionar categoría</option>
                        ${categoriasOptions}
                    </select>
                    <p id="form-error" style="color: #ef4444; font-size: 0.85rem; display: none;"></p>
                    <div class="dialog-actions">
                        <button type="button" class="btn btn-danger btn-sm" id="btn-cancel-modal">Cancelar</button>
                        <button type="submit" class="btn btn-success btn-sm" id="btn-save-product">Guardar</button>
                    </div>
                </form>
            </dialog>
        `;

        // Búsqueda en tiempo real
        const searchInput = document.getElementById('search-input') as HTMLInputElement;
        searchInput?.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();
            const rows = document.querySelectorAll('#productos-tbody tr');
            rows.forEach(row => {
                const text = row.textContent?.toLowerCase() || '';
                (row as HTMLElement).style.display = text.includes(query) ? '' : 'none';
            });
        });

    } catch (error) {
        container.innerHTML = '<h2 style="color: #ef4444;">Error cargando la API</h2><p style="color: #9ca3af;">Verifica que el backend esté corriendo.</p>';
    }
}
