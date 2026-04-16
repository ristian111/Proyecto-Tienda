import './style.css';
import { renderLogin } from './views/login';
import { renderInventory } from './views/inventario';
import { renderNewSale } from './views/venta';
import { renderPurchases } from './views/compras';
import { renderSidebar } from './components/navbar';
import { renderInvoices } from './views/facturas';
import { renderMisc } from './views/misc';
import { renderStatistics } from './views/estadisticas';
import { api } from './api/endpoints';

const app = document.querySelector<HTMLDivElement>('#app')!;

function checkAuth() {
    return localStorage.getItem('token') !== null;
}

export function router() {
    const hash = window.location.hash;

    if (!checkAuth()) {
        if (hash !== '#/login') {
            window.location.hash = '#/login';
            return;
        }
        app.className = 'login-mode';
        app.innerHTML = renderLogin();
        return;
    }

    if (hash === '#/login' || hash === '') {
        window.location.hash = '#/venta';
        return;
    }

    app.className = 'dashboard-mode';

    app.innerHTML = `
        ${renderSidebar(hash)}
        <main class="main-content" id="content"></main>
    `;

    const content = document.getElementById('content')!;

    if (hash === '#/venta') {
        renderNewSale(content);
    } else if (hash === '#/compras') {
        renderPurchases(content);
    } else if (hash === '#/inventario') {
        renderInventory(content);
    } else if (hash === '#/pedidos') {
        content.innerHTML = '<h1>Pedidos</h1><p class="placeholder-text">Nada por aqui...</p>';
    } else if (hash === '#/facturas') {
        renderInvoices(content);
    } else if (hash === '#/estadisticas') {
        renderStatistics(content);
    } else if (hash === '#/misc') {
        renderMisc(content);
    }
}

window.addEventListener('hashchange', router);
router();

document.addEventListener('click', async (e) => {
    const target = e.target as HTMLElement;

    if (target.id === 'btn-logout') {
        localStorage.removeItem('token');
        window.location.hash = '';
        router();
    }

    if (target.classList.contains('btn-delete')) {
        const uuid = target.getAttribute('data-uuid');
        if (uuid && confirm(`¿Seguro que quieres eliminar este producto?`)) {
            try {
                await api.deleteProduct(uuid);
                const content = document.getElementById('content');
                if (content) renderInventory(content);
            } catch (err: any) {
                alert(err.message || 'Error al eliminar');
            }
        }
    }

    if (target.classList.contains('btn-edit')) {
        const modal = document.getElementById('product-modal') as HTMLDialogElement;
        if (!modal) return;

        const title = document.getElementById('modal-title');
        if (title) title.textContent = 'Editar Producto';

        (document.getElementById('product-uuid') as HTMLInputElement).value = target.dataset.uuid || '';
        (document.getElementById('product-nombre') as HTMLInputElement).value = target.dataset.nombre || '';
        (document.getElementById('product-precio-venta') as HTMLInputElement).value = target.dataset.precioVenta || '';
        (document.getElementById('product-precio-compra') as HTMLInputElement).value = target.dataset.precioCompra || '';
        (document.getElementById('product-unidad') as HTMLInputElement).value = target.dataset.unidad || '';
        (document.getElementById('product-categoria') as HTMLSelectElement).value = target.dataset.categoria || '';

        const containerCA = document.getElementById('container-cantidad-actual');
        const inputCA = document.getElementById('product-cantidad-actual') as HTMLInputElement;
        if (containerCA) containerCA.style.display = 'none';
        if (inputCA) {
            inputCA.required = false;
            inputCA.value = '';
        }

        const errorEl = document.getElementById('form-error');
        if (errorEl) errorEl.style.display = 'none';

        modal.showModal();
    }

    if (target.id === 'btn-add-product') {
        const modal = document.getElementById('product-modal') as HTMLDialogElement;
        if (!modal) return;

        const title = document.getElementById('modal-title');
        if (title) title.textContent = 'Nuevo Producto';

        (document.getElementById('product-uuid') as HTMLInputElement).value = '';
        (document.getElementById('product-nombre') as HTMLInputElement).value = '';
        (document.getElementById('product-precio-venta') as HTMLInputElement).value = '';
        (document.getElementById('product-precio-compra') as HTMLInputElement).value = '';
        (document.getElementById('product-unidad') as HTMLInputElement).value = '';
        (document.getElementById('product-categoria') as HTMLSelectElement).value = '';

        const containerCA = document.getElementById('container-cantidad-actual');
        const inputCA = document.getElementById('product-cantidad-actual') as HTMLInputElement;
        if (containerCA) containerCA.style.display = 'block';
        if (inputCA) {
            inputCA.required = true;
            inputCA.value = '';
        }

        const errorEl = document.getElementById('form-error');
        if (errorEl) errorEl.style.display = 'none';

        modal.showModal();
    }

    if (target.id === 'btn-cancel-modal') {
        const modal = document.getElementById('product-modal') as HTMLDialogElement;
        if (modal) modal.close();
    }

    if (target.classList.contains('btn-delete-cat')) {
        const uuid = target.getAttribute('data-uuid');
        if (uuid && confirm(`¿Seguro que quieres eliminar esta categoría?`)) {
            try {
                await api.deleteCategory(uuid);
                const content = document.getElementById('content');
                if (content) renderMisc(content);
            } catch (err: any) {
                alert(err.message || 'Error al eliminar');
            }
        }
    }

    if (target.classList.contains('btn-edit-cat')) {
        const modal = document.getElementById('category-modal') as HTMLDialogElement;
        if (!modal) return;
        const title = document.getElementById('modal-cat-title');
        if (title) title.textContent = 'Editar Categoría';

        (document.getElementById('cat-uuid') as HTMLInputElement).value = target.dataset.uuid || '';
        (document.getElementById('cat-nombre') as HTMLInputElement).value = target.dataset.nombre || '';
        (document.getElementById('cat-descripcion') as HTMLInputElement).value = target.dataset.descripcion || '';

        const errorEl = document.getElementById('form-cat-error');
        if (errorEl) errorEl.style.display = 'none';
        modal.showModal();
    }

    if (target.id === 'btn-add-category') {
        const modal = document.getElementById('category-modal') as HTMLDialogElement;
        if (!modal) return;
        const title = document.getElementById('modal-cat-title');
        if (title) title.textContent = 'Nueva Categoría';

        (document.getElementById('cat-uuid') as HTMLInputElement).value = '';
        (document.getElementById('cat-nombre') as HTMLInputElement).value = '';
        (document.getElementById('cat-descripcion') as HTMLInputElement).value = '';

        const errorEl = document.getElementById('form-cat-error');
        if (errorEl) errorEl.style.display = 'none';
        modal.showModal();
    }

    if (target.id === 'btn-cancel-cat') {
        const modal = document.getElementById('category-modal') as HTMLDialogElement;
        if (modal) modal.close();
    }
});

document.addEventListener('submit', async (e) => {
    const target = e.target as HTMLFormElement;

    if (target.id === 'product-form') {
        e.preventDefault();

        const uuid = (document.getElementById('product-uuid') as HTMLInputElement).value;
        const nombre = (document.getElementById('product-nombre') as HTMLInputElement).value.trim();
        const precio_venta = parseFloat((document.getElementById('product-precio-venta') as HTMLInputElement).value);
        const costo_promedio = parseFloat((document.getElementById('product-precio-compra') as HTMLInputElement).value);
        const unidad_medida = (document.getElementById('product-unidad') as HTMLInputElement).value.trim();
        const ref_categoria = (document.getElementById('product-categoria') as HTMLSelectElement).value;

        const errorEl = document.getElementById('form-error')!;
        const btnSave = document.getElementById('btn-save-product') as HTMLButtonElement;

        errorEl.style.display = 'none';
        btnSave.disabled = true;
        btnSave.textContent = 'Guardando...';

        const data: any = { nombre, precio_venta, costo_promedio, unidad_medida, ref_categoria };

        if (!uuid) {
            data.cantidad_actual = parseInt((document.getElementById('product-cantidad-actual') as HTMLInputElement).value) || 0;
        }

        try {
            if (uuid) {
                await api.updateProduct(uuid, data);
            } else {
                await api.createProduct(data);
            }

            const modal = document.getElementById('product-modal') as HTMLDialogElement;
            if (modal) modal.close();

            const content = document.getElementById('content');
            if (content) renderInventory(content);
        } catch (err: any) {
            errorEl.textContent = err.message || 'Error al guardar';
            errorEl.style.display = 'block';
        } finally {
            btnSave.disabled = false;
            btnSave.textContent = 'Guardar';
        }
    }

    if (target.id === 'category-form') {
        e.preventDefault();

        const uuid = (document.getElementById('cat-uuid') as HTMLInputElement).value;
        const nombre = (document.getElementById('cat-nombre') as HTMLInputElement).value.trim();
        const descripcion = (document.getElementById('cat-descripcion') as HTMLInputElement).value.trim();

        const errorEl = document.getElementById('form-cat-error')!;
        const btnSave = document.getElementById('btn-save-cat') as HTMLButtonElement;

        errorEl.style.display = 'none';
        btnSave.disabled = true;
        btnSave.textContent = 'Guardando...';

        const data = { nombre, descripcion };

        try {
            if (uuid) {
                await api.updateCategory(uuid, data);
            } else {
                await api.createCategory(data);
            }

            const modal = document.getElementById('category-modal') as HTMLDialogElement;
            if (modal) modal.close();

            const content = document.getElementById('content');
            if (content) renderMisc(content);
        } catch (err: any) {
            errorEl.textContent = err.message || 'Error al guardar';
            errorEl.style.display = 'block';
        } finally {
            btnSave.disabled = false;
            btnSave.textContent = 'Guardar';
        }
    }
});
