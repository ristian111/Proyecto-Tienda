// ———— Imports & Globals ————

import { api } from '../api/endpoints';

// No cambias nada de aqui, cristian. Esto lo voy a migrar pa otro lado xd.
declare var Chart: any;

let chartTopProducts: any = null;
let chartCategories: any = null;
let chartRevenues: any = null;

// ———— Main Render Function ————

// Renders the main HTML structure and attaches initial event listeners
export function renderStatistics(container: HTMLElement) {
    container.innerHTML = `
        <div class="dashboard-header">
            <h2>Estadísticas</h2>
        </div>
        
        <div class="stats-grid">
            <div class="card-container stat-card">
                <h3 class="stat-title">Ventas Hoy</h3>
                <h2 id="sales-today" class="stat-value stat-green">$0.00</h2>
            </div>
            <div class="card-container stat-card">
                <h3 class="stat-title">Ganancia Hoy</h3>
                <h2 id="profit-today" class="stat-value stat-blue">$0.00</h2>
            </div>
            <div class="card-container stat-card">
                <h3 class="stat-title">Ticket Promedio</h3>
                <h2 id="average-ticket" class="stat-value stat-orange">$0.00</h2>
            </div>
        </div>

        <div class="charts-grid-half">
            <div class="card-container">
                <h3 class="section-title">Ventas por Categoría</h3>
                <canvas id="chart-categories" class="chart-canvas"></canvas>
            </div>
            <div class="card-container">
                <div class="chart-header">
                    <h3 class="section-title" style="margin:0;">Top 5 Productos</h3>
                    <select id="filter-top-products" class="filter-select">
                        <option value="diario">Hoy</option>
                        <option value="semanal">Esta Semana</option>
                        <option value="mensual" selected>Este Mes</option>
                    </select>
                </div>
                <canvas id="chart-top-products" class="chart-canvas"></canvas>
            </div>
        </div>
        
        <div class="charts-grid-full">
            <div class="card-container">
                <h3 class="section-title">Ventas vs Ganancia (7 días)</h3>
                <canvas id="chart-revenues" class="chart-canvas"></canvas>
            </div>
        </div>
        
        <div class="card-container">
            <h3 class="section-title section-title-warning">
                <i class='bx bx-error-circle'></i> Estancados (+30 días)
            </h3>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Ref</th>
                        <th>Producto</th>
                        <th>Días sin vender</th>
                        <th>Stock</th>
                    </tr>
                </thead>
                <tbody id="stagnant-list">
                </tbody>
            </table>
            <p id="msg-stagnant-empty" class="empty-message">Nada por aqui.</p>
        </div>
    `;

    // Delays execution slightly to ensure DOM nodes are fully mounted
    setTimeout(() => {
        loadStatistics();
        document.getElementById('filter-top-products')?.addEventListener('change', (e) => {
            const value = (e.target as HTMLSelectElement).value;
            loadTopProducts(value);
        });
    }, 50);
}

// ———— Utilities ————

// Formats a numeric value to COP currency format
const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CO', { 
        style: 'currency', 
        currency: 'COP', 
        minimumFractionDigits: 0 
    }).format(amount);
};

// ———— Data Fetching & Processing ————

// Fetches all statistical data concurrently and updates the UI components
async function loadStatistics() {
    try {
        const [summary, topProducts, revenues, stagnantProducts, categories] = await Promise.all([
            api.getResumenHoy(),
            api.getTopProductos('mensual'),
            api.getIngresosGanancias(7),
            api.getProductosEstancados(),
            api.getPorcentajeCategorias()
        ]);

        const formatValue = (val: any) => formatCurrency(parseFloat(val || 0));

        // Update top statistics cards
        document.getElementById('sales-today')!.textContent = formatValue(summary.ventas_hoy);
        document.getElementById('profit-today')!.textContent = formatValue(summary.ganancia_hoy);
        document.getElementById('average-ticket')!.textContent = formatValue(summary.ticket_promedio);

        // Update charts
        renderCategoriesChart(categories);
        renderTopProductsChart(topProducts);
        renderRevenuesChart(revenues);

        // Update table
        renderStagnantTable(stagnantProducts);

    } catch (err: any) {
        console.error('Error al cargar estadísticas', err);
    }
}

// Fetches top products based on selected filter and updates the respective chart
async function loadTopProducts(filter: string) {
    try {
        const topProducts = await api.getTopProductos(filter);
        renderTopProductsChart(topProducts);
    } catch (err: any) {
        console.error(err);
    }
}

// ———— UI Updaters ————

// Renders the categories pie chart
function renderCategoriesChart(categories: any[]) {
    const canvasContext = document.getElementById('chart-categories') as HTMLCanvasElement;
    if (chartCategories) chartCategories.destroy();
    
    const config = createPieChartConfig(categories);
    chartCategories = new Chart(canvasContext, config);
}

// Renders the top products bar chart
function renderTopProductsChart(topProducts: any[]) {
    const canvasContext = document.getElementById('chart-top-products') as HTMLCanvasElement;
    if (chartTopProducts) chartTopProducts.destroy();
    
    const config = createBarChartConfig(topProducts);
    chartTopProducts = new Chart(canvasContext, config);
}

// Renders the revenues line chart
function renderRevenuesChart(revenues: any[]) {
    const canvasContext = document.getElementById('chart-revenues') as HTMLCanvasElement;
    if (chartRevenues) chartRevenues.destroy();
    
    const config = createLineChartConfig(revenues);
    chartRevenues = new Chart(canvasContext, config);
}

// Populates the stagnant products table
function renderStagnantTable(stagnantProducts: any[]) {
    const tableBody = document.getElementById('stagnant-list')!;
    const emptyMessage = document.getElementById('msg-stagnant-empty')!;
    
    tableBody.innerHTML = '';
    
    if (stagnantProducts.length === 0) {
        emptyMessage.style.display = 'block';
    } else {
        emptyMessage.style.display = 'none';
        stagnantProducts.forEach((product: any) => {
            const tableRow = document.createElement('tr');
            tableRow.innerHTML = `
                <td>${product.ref}</td>
                <td>${product.nombre}</td>
                <td class="text-danger">${product.dias_estancado ?? 'None'} días</td> 
                <td>${product.stock ?? 0} unds.</td>
            `;
            tableBody.appendChild(tableRow); // Hay que cambiar la vaina esa de "nunca" dias, esta feo asi.
        });
    }
}

// ———— Chart Configuration Factories ————

// Generates configuration object for the pie chart
function createPieChartConfig(categories: any[]) {
    return {
        type: 'pie',
        data: {
            labels: categories.map((c: any) => c.nombre),
            datasets:[{
                data: categories.map((c: any) => c.vendidos),
                backgroundColor:['#3498db', '#e74c3c', '#f1c40f', '#2ecc71', '#9b59b6', '#e67e22', '#1abc9c']
            }]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { 
                legend: { labels: { color: '#ccc' } } 
            } 
        }
    };
}

// Generates configuration object for the bar chart
function createBarChartConfig(topProducts: any[]) {
    return {
        type: 'bar',
        data: {
            labels: topProducts.map((p: any) => p.nombre.length > 15 ? p.nombre.substring(0, 15) + "..." : p.nombre),
            datasets:[{
                label: 'Unidades Vendidas',
                data: topProducts.map((p: any) => p.cantidad),
                backgroundColor: '#9b59b6'
            }]
        },
        options: { 
            indexAxis: 'y', 
            responsive: true, 
            maintainAspectRatio: false,
            plugins: { 
                legend: { labels: { color: '#ccc' } } 
            },
            scales: { 
                x: { beginAtZero: true, ticks: { color: '#999' }, grid: { color: '#2a2a2e' } }, 
                y: { ticks: { color: '#ccc' }, grid: { color: '#2a2a2e' } } 
            }
        }
    };
}

// Generates configuration object for the line chart
function createLineChartConfig(revenues: any[]) {
    return {
        type: 'line',
        data: {
            labels: revenues.map((i: any) => i.fecha.slice(5)),
            datasets:[
                {
                    label: 'Ventas',
                    data: revenues.map((i: any) => i.ingreso),
                    borderColor: '#2ecc71',
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
                    fill: true,
                    tension: 0.3
                },
                {
                    label: 'Ganancia',
                    data: revenues.map((i: any) => i.ganancia),
                    borderColor: '#3498db',
                    backgroundColor: 'transparent',
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.3
                }
            ]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { 
                legend: { labels: { color: '#ccc' } } 
            }, 
            scales: { 
                x: { ticks: { color: '#999' }, grid: { color: '#2a2a2e' } }, 
                y: { ticks: { color: '#999' }, grid: { color: '#2a2a2e' } } 
            } 
        }
    };
}
