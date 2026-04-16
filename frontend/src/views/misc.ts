import { api } from '../api/endpoints';

export async function renderMisc(container: HTMLElement) {
    container.innerHTML = '<h2 style="color: #4b5563; padding-top: 40px;">Cargando misceláneas...</h2>';

    try {
        const categories = await api.getCategories();

        const rowsHTML = categories.map(c => `
            <tr>
                <td style="color: #6b7280; font-weight: 500; font-size: 0.75rem;" title="${c.ref}">${c.ref.slice(0, 8)}…</td>
                <td style="font-weight: 500; color: #f3f4f6;">${c.nombre}</td>
                <td style="color: #9ca3af;">${c.descripcion || '-'}</td>
                <td>
                    <button class="btn btn-warning btn-sm btn-edit-cat"
                        data-uuid="${c.ref}"
                        data-nombre="${c.nombre}"
                        data-descripcion="${c.descripcion}">Editar</button>
                    <button class="btn btn-danger btn-sm btn-delete-cat" data-uuid="${c.ref}" style="margin-left: 6px;">Eliminar</button>
                </td>
            </tr>
        `).join('');

        container.innerHTML = `
            <div class="page-header">
                <h1>Categorias</h1>
                <button class="btn btn-success" id="btn-add-category">+ Nueva Categoría</button>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody id="categorias-tbody">
                    ${rowsHTML}
                </tbody>
            </table>
            
            <!-- Category Modal -->
            <dialog id="category-modal">
                <h2 id="modal-cat-title">Nueva Categoría</h2>
                <form id="category-form">
                    <input type="hidden" id="cat-uuid">
                    <input type="text" id="cat-nombre" placeholder="Nombre de la categoría" required>
                    <input type="text" id="cat-descripcion" placeholder="Descripción breve" required>
                    <p id="form-cat-error" style="color: #ef4444; font-size: 0.85rem; display: none;"></p>
                    <div class="dialog-actions">
                        <button type="button" class="btn btn-danger btn-sm" id="btn-cancel-cat">Cancelar</button>
                        <button type="submit" class="btn btn-success btn-sm" id="btn-save-cat">Guardar</button>
                    </div>
                </form>
            </dialog>
        `;

    } catch (error) {
        container.innerHTML = '<h2 style="color: #ef4444;">Error cargando categorías</h2><p style="color: #9ca3af;">Verifica que el backend esté corriendo.</p>';
    }
}
