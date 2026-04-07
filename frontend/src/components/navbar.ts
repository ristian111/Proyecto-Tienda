export function renderSidebar(activeRoute: string = '') {
    const links = [
        { hash: '#/venta',      label: 'Venta',      icon: "<i class='bx bx-dollar-circle'></i>" },
        { hash: '#/compras',    label: 'Compras',    icon: "<i class='bx bx-archive-in'></i>" },
        { hash: '#/inventario', label: 'Inventario', icon: "<i class='bx bx-package'></i>" },
        { hash: '#/pedidos',    label: 'Pedidos',    icon: "<i class='bx bx-cart'></i>" },
        { hash: '#/facturas',   label: 'Facturas',   icon: "<i class='bx bx-receipt'></i>" },
        { hash: '#/estadisticas', label: 'Estadísticas', icon: "<i class='bx bx-chart'></i>" },
        { hash: '#/misc',       label: 'Misc',       icon: "<i class='bx bx-cog'></i>" },
    ];

    const navHTML = links.map(l => `
        <a href="${l.hash}" class="nav-link ${activeRoute === l.hash ? 'active' : ''}">
            <span class="icon">${l.icon}</span>
            ${l.label}
        </a>
    `).join('');

    return `
        <aside class="sidebar">
            <div class="sidebar-brand">
                <span style="font-size: 1.4rem; transform: translateY(2px);"><i class='bx bxs-store-alt'></i></span> Mi Tienda
            </div>
            ${navHTML}
            <div class="sidebar-footer">
                <button id="btn-logout" class="btn btn-danger" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;">
                    <i class='bx bx-log-out' style="font-size: 1.1rem;"></i> Cerrar Sesión
                </button>
            </div>
        </aside>
    `;
}
