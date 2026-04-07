// Base URL vacía — las peticiones van a /v1/... y Vite las proxea al backend
export const API_URL = '';

export const getAuthHeaders = (): Record<string, string> => {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
};
