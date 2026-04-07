import { api } from '../api/endpoints';

declare var Chart: any;

let chartTopProductos: any = null;
let chartCategorias: any = null;
let chartIngresos: any = null;
let chartHoras: any = null;

export function renderEstadisticas(container: HTMLElement) {
    container.innerHTML = `
        <div class="header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
            <h2>Estadísticas</h2>
        </div>
        
        <div class="stats-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px;">
            <div class="stat-card" style="background:#1c1c20; padding:20px; border-radius:8px; border:1px solid #2a2a2e; text-align:center;">
                <h3 style="color:#999; font-size:13px; margin-bottom:10px;">Ventas Hoy</h3>
                <h2 id="ventas-hoy" style="color:#2ecc71; font-size:24px;">$0.00</h2>
            </div>
            <div class="stat-card" style="background:#1c1c20; padding:20px; border-radius:8px; border:1px solid #2a2a2e; text-align:center;">
                <h3 style="color:#999; font-size:13px; margin-bottom:10px;">Ganancia Hoy</h3>
                <h2 id="ganancia-hoy" style="color:#3498db; font-size:24px;">$0.00</h2>
            </div>
            <div class="stat-card" style="background:#1c1c20; padding:20px; border-radius:8px; border:1px solid #2a2a2e; text-align:center;">
                <h3 style="color:#999; font-size:13px; margin-bottom:10px;">Ticket Promedio</h3>
                <h2 id="ticket-promedio" style="color:#e67e22; font-size:24px;">$0.00</h2>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
            <div style="background:#1c1c20; padding:20px; border-radius:8px; border:1px solid #2a2a2e;">
                <h3 style="margin-bottom: 15px; font-size: 15px; color:#e0e0e0;">Ventas por Categoría</h3>
                <canvas id="chart-categorias" style="max-height: 250px;"></canvas>
            </div>
            <div style="background:#1c1c20; padding:20px; border-radius:8px; border:1px solid #2a2a2e;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 15px;">
                    <h3 style="font-size: 15px; color:#e0e0e0;">Top 5 Productos</h3>
                    <select id="filtro-top-productos" style="padding: 5px; border-radius: 4px; border: 1px solid #3a3a3e; background:#16161a; color:#ccc; font-size:12px;">
                        <option value="diario">Hoy</option>
                        <option value="semanal">Esta Semana</option>
                        <option value="mensual" selected>Este Mes</option>
                    </select>
                </div>
                <canvas id="chart-top-productos" style="max-height: 250px;"></canvas>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px;">
            <div style="background:#1c1c20; padding:20px; border-radius:8px; border:1px solid #2a2a2e;">
                <h3 style="margin-bottom: 15px; font-size: 15px; color:#e0e0e0;">Ventas vs Ganancia (7 días)</h3>
                <canvas id="chart-ingresos" style="max-height: 250px;"></canvas>
            </div>
            <div style="background:#1c1c20; padding:20px; border-radius:8px; border:1px solid #2a2a2e;">
                <h3 style="margin-bottom: 15px; font-size: 15px; color:#e0e0e0;">Horas Pico</h3>
                <canvas id="chart-horas" style="max-height: 250px;"></canvas>
            </div>
        </div>
        
        <div style="background:#1c1c20; padding:20px; border-radius:8px; border:1px solid #2a2a2e; margin-bottom:20px;">
            <h3 style="color:#e74c3c; margin-bottom: 15px; font-size: 15px;">
                <i class='bx bx-error-circle'></i> Estancados (+30 días)
            </h3>
            <table class="table" style="width: 100%; border-collapse: separate; border-spacing: 0;">
                <thead>
                    <tr style="background:#16161a;">
                        <th style="padding: 10px; border-bottom: 1px solid #2a2a2e; text-align: left; border-top-left-radius: 4px; color:#999;">Ref</th>
                        <th style="padding: 10px; border-bottom: 1px solid #2a2a2e; text-align: left; color:#999;">Producto</th>
                        <th style="padding: 10px; border-bottom: 1px solid #2a2a2e; text-align: left; border-top-right-radius: 4px; color:#999;">Acción</th>
                    </tr>
                </thead>
                <tbody id="lista-estancados">
                </tbody>
            </table>
            <p id="msg-estancados-vacio" style="color: #888; margin-top: 10px; display: none;">¡Excelente! No tienes productos estancados.</p>
        </div>
    `;

    setTimeout(() => {
        loadEstadisticas();
        document.getElementById('filtro-top-productos')?.addEventListener('change', (e) => {
            const value = (e.target as HTMLSelectElement).value;
            loadTopProductos(value);
        });
    }, 50);
}

const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(amount);
};

async function loadEstadisticas() {
    try {
        const [resumen, topProd, ingresos, horasPico, estancados, categorias] = await Promise.all([
            api.getResumenHoy(),
            api.getTopProductos('mensual'),
            api.getIngresosGanancias(7),
            api.getHorasPico(),
            api.getProductosEstancados(),
            api.getPorcentajeCategorias()
        ]);

        const formatC = (val: any) => formatCurrency(parseFloat(val || 0));

        document.getElementById('ventas-hoy')!.textContent = formatC(resumen.ventas_hoy);
        document.getElementById('ganancia-hoy')!.textContent = formatC(resumen.ganancia_hoy);
        document.getElementById('ticket-promedio')!.textContent = formatC(resumen.ticket_promedio);

        const ctxCat = document.getElementById('chart-categorias') as HTMLCanvasElement;
        if (chartCategorias) chartCategorias.destroy();
        chartCategorias = new Chart(ctxCat, {
            type: 'pie',
            data: {
                labels: categorias.map((c: any) => c.nombre),
                datasets: [{
                    data: categorias.map((c: any) => c.vendidos),
                    backgroundColor: ['#3498db', '#e74c3c', '#f1c40f', '#2ecc71', '#9b59b6', '#e67e22', '#1abc9c']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#ccc' } } } }
        });

        renderTopProductos(topProd);

        const ctxIngresos = document.getElementById('chart-ingresos') as HTMLCanvasElement;
        if (chartIngresos) chartIngresos.destroy();
        chartIngresos = new Chart(ctxIngresos, {
            type: 'line',
            data: {
                labels: ingresos.map((i: any) => i.fecha.slice(5)),
                datasets: [
                    {
                        label: 'Ventas',
                        data: ingresos.map((i: any) => i.ingreso),
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Ganancia',
                        data: ingresos.map((i: any) => i.ganancia),
                        borderColor: '#3498db',
                        backgroundColor: 'transparent',
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0.3
                    }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#ccc' } } }, scales: { x: { ticks: { color: '#999' }, grid: { color: '#2a2a2e' } }, y: { ticks: { color: '#999' }, grid: { color: '#2a2a2e' } } } }
        });

        const ctxHoras = document.getElementById('chart-horas') as HTMLCanvasElement;
        if (chartHoras) chartHoras.destroy();
        chartHoras = new Chart(ctxHoras, {
            type: 'bar',
            data: {
                labels: horasPico.map((h: any) => h.hora),
                datasets: [{
                    label: '# Ventas',
                    data: horasPico.map((h: any) => h.ventas),
                    backgroundColor: '#e67e22'
                }]
            },
            options: { 
                responsive: true, 
                maintainAspectRatio: false,
                plugins: { legend: { labels: { color: '#ccc' } } },
                scales: { y: { beginAtZero: true, ticks: { stepSize: 1, color: '#999' }, grid: { color: '#2a2a2e' } }, x: { ticks: { color: '#999' }, grid: { color: '#2a2a2e' } } }
            }
        });

        const tbody = document.getElementById('lista-estancados')!;
        const emptyMsg = document.getElementById('msg-estancados-vacio')!;
        tbody.innerHTML = '';
        if (estancados.length === 0) {
            emptyMsg.style.display = 'block';
        } else {
            emptyMsg.style.display = 'none';
            estancados.forEach((p: any) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="padding: 10px; border-bottom: 1px solid #2a2a2e; color:#ccc;">${p.ref}</td>
                    <td style="padding: 10px; border-bottom: 1px solid #2a2a2e; color:#ccc;">${p.nombre}</td>
                    <td style="padding: 10px; border-bottom: 1px solid #2a2a2e;"><span style="color:#e74c3c; font-weight:bold;">¡Hacer Promo!</span></td>
                `;
                tbody.appendChild(tr);
            });
        }

    } catch (err: any) {
        console.error('Error al cargar estadísticas', err);
    }
}

async function loadTopProductos(filtro: string) {
    try {
        const topProd = await api.getTopProductos(filtro);
        renderTopProductos(topProd);
    } catch (err: any) {
        console.error(err);
    }
}

function renderTopProductos(topProd: any[]) {
    const ctxTop = document.getElementById('chart-top-productos') as HTMLCanvasElement;
    if (chartTopProductos) chartTopProductos.destroy();
    chartTopProductos = new Chart(ctxTop, {
        type: 'bar',
        data: {
            labels: topProd.map((p: any) => p.nombre.length > 15 ? p.nombre.substring(0,15)+"..." : p.nombre),
            datasets: [{
                label: 'Unidades Vendidas',
                data: topProd.map((p: any) => p.cantidad),
                backgroundColor: '#9b59b6'
            }]
        },
        options: { 
            indexAxis: 'y', 
            responsive: true, 
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#ccc' } } },
            scales: { x: { beginAtZero: true, ticks: { color: '#999' }, grid: { color: '#2a2a2e' } }, y: { ticks: { color: '#ccc' }, grid: { color: '#2a2a2e' } } }
        }
    });
}
