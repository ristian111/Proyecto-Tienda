// Placeholder para el componente de tabla
export function renderTable(headers: string[], bodyHtml: string) {
    return `
        <table>
            <thead>
                <tr>
                    ${headers.map(h => `<th>${h}</th>`).join('')}
                </tr>
            </thead>
            <tbody>
                ${bodyHtml}
            </tbody>
        </table>
    `;
}
