import { api } from '../api/endpoints';

function priceBadge(price: number | string): string {
    return `<span class="cell-price">$${Number(price).toFixed(2)}</span>`;
}


export async function renderInventory(container: HTMLElement) {
    container.innerHTML = '<h2 class="loading-state">Cargando inventario...</h2>';

    try {
        const [products, categories, inventories] = await Promise.all([
            api.getProducts(),
            api.getCategories(),
            api.getInventories(),
        ]);

        const qtyPerProduct: Record<string, number> = {};
        inventories.forEach(inv => {
            qtyPerProduct[inv.ref_producto] = inv.cantidad_actual;
        });


        const rowsHTML = products.map(p => `
            <tr>
                <td class="cell-ref" title="${p.ref}">${p.ref.slice(0, 8)}…</td>
                <td class="cell-name">${p.nombre}</td>
                <td>${priceBadge(p.precio_venta)}</td>
                <td class="cell-cost">$${Number(p.costo_promedio).toFixed(2)}</td>
                <td class="cell-unit">${p.unidad_medida}</td>
                <td class="cell-stock">${qtyPerProduct[p.ref] ?? 0}</td>
                <td>
                    <button class="btn btn-warning btn-sm btn-edit"
                        data-uuid="${p.ref}"
                        data-nombre="${p.nombre}"
                        data-precio-venta="${p.precio_venta}"
                        data-precio-compra="${p.costo_promedio}"
                        data-unidad="${p.unidad_medida}"
                        data-categoria="${p.ref_categoria}">Editar</button>
                    <button class="btn btn-danger btn-sm btn-delete ml-6" data-uuid="${p.ref}">Eliminar</button>
                </td>
            </tr>
        `).join('');

        const categoriesOptions = categories.map(c =>
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
                    ${rowsHTML}
                </tbody>
            </table>
            
            <dialog id="product-modal">
                <h2 id="modal-title">Nuevo Producto</h2>
                <form id="product-form">
                    <input type="hidden" id="product-uuid">
                    <input type="text" id="product-nombre" placeholder="Nombre del producto" required>
                    <input type="number" id="product-precio-venta" placeholder="Precio de venta" step="0.01" min="0" required>
                    <input type="number" id="product-precio-compra" placeholder="Precio de compra" step="0.01" min="0" required>
                    <input type="text" id="product-unidad" placeholder="Unidad de medida (ej: unidad, kg)" required>
                    <div id="container-cantidad-actual" class="container-cantidad-actual">
                        <input type="number" id="product-cantidad-actual" placeholder="Cantidad actual en inventario" step="1" min="0" required>
                    </div>
                    <select id="product-categoria" required>
                        <option value="" disabled selected>Seleccionar categoría</option>
                        ${categoriesOptions}
                    </select>
                    <p id="form-error" class="form-error"></p>
                    <div class="dialog-actions">
                        <button type="button" class="btn btn-danger btn-sm" id="btn-cancel-modal">Cancelar</button>
                        <button type="submit" class="btn btn-success btn-sm" id="btn-save-product">Guardar</button>
                    </div>
                </form>
            </dialog>
        `;


        // Search filter
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
        container.innerHTML = '<h2 class="error-state">Error cargando la API</h2><p class="error-hint">Verifica que el backend esté corriendo.</p>';
    }
}
