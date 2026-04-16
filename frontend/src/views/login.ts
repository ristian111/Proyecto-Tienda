import { api } from '../api/endpoints';

export function renderLogin() {
    return `
        <div class="login-card">
            <h2>Bienvenido de vuelta</h2>
            <p class="subtitle">Inicia sesión</p>
            <form id="login-form">
                <input type="text" id="username" placeholder="Usuario" required>
                <input type="password" id="password" placeholder="Contraseña" required>
                <p id="login-error" class="form-error"></p>
                <button type="submit" class="btn btn-fullwidth" id="btn-login">
                    Submit →
                </button>
            </form>
        </div>
    `;
}

// Listen for submit at a global level
document.addEventListener('submit', async (e) => {
    const target = e.target as HTMLFormElement;
    if (target.id === 'login-form') {
        e.preventDefault();

        const username = (document.getElementById('username') as HTMLInputElement).value.trim();
        const password = (document.getElementById('password') as HTMLInputElement).value;
        const errorEl = document.getElementById('login-error')!;
        const btnLogin = document.getElementById('btn-login') as HTMLButtonElement;

        btnLogin.disabled = true;
        btnLogin.textContent = 'Conectando...';
        errorEl.style.display = 'none';

        try {
            const data = await api.login(username, password);
            localStorage.setItem('token', data.token);
            window.location.hash = '#/inventario';
        } catch (err: any) {
            errorEl.textContent = err.message || 'Credenciales inválidas';
            errorEl.style.display = 'block';
        } finally {
            btnLogin.disabled = false;
            btnLogin.textContent = 'Entrar al Panel →';
        }
    }
});
