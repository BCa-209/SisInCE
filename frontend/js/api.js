import { API_URL, AUTH_URL } from './config.js';

export class SessionExpiredError extends Error {
    constructor(message = 'Sesión expirada o no autorizada') {
        super(message);
        this.name = 'SessionExpiredError';
    }
}

/**
 * Inicia sesión enviando nombres, apellidos y código al backend.
 * La sesión se administra mediante cookie HttpOnly.
 */
export async function login(nombres, apellidos, codigo) {
    const response = await fetch(`${AUTH_URL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
            nombres: nombres.trim(),
            apellidos: apellidos.trim(),
            codigo: codigo.trim()
        })
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.detail || 'Error al iniciar sesión');
    }
    return data;
}

/**
 * Cierra la sesión activa en el servidor e invalida la cookie HttpOnly.
 */
export async function logout() {
    try {
        const response = await fetch(`${AUTH_URL}/logout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({})
        });
        return await response.json();
    } catch (e) {
        console.error('Error durante el cierre de sesión:', e);
        return { message: 'Sesión local cerrada' };
    }
}

/**
 * Verifica si hay una sesión activa y devuelve el perfil del estudiante.
 */
export async function fetchCurrentUser() {
    const response = await fetch(`${AUTH_URL}/me`, {
        method: 'GET',
        credentials: 'include'
    });

    if (response.status === 401) {
        return null;
    }

    if (!response.ok) {
        throw new Error('Error al verificar sesión actual');
    }

    return await response.json();
}

/**
 * Consulta la lista de estudiantes según los filtros proporcionados.
 */
export async function fetchEstudiantes(url) {
    const response = await fetch(url, {
        credentials: 'include'
    });

    if (response.status === 401) {
        throw new SessionExpiredError('Su sesión ha vencido por inactividad. Por favor ingrese nuevamente.');
    }

    if (!response.ok) {
        throw new Error('No se encontraron resultados');
    }

    const data = await response.json();
    return Array.isArray(data) ? data : [data];
}

/**
 * Obtiene el catálogo de facultades registradas.
 */
export async function fetchFacultades() {
    try {
        const response = await fetch(`${API_URL}/facultades`, {
            credentials: 'include'
        });
        if (response.status === 401) throw new SessionExpiredError();
        if (!response.ok) return [];
        return await response.json();
    } catch (e) {
        if (e instanceof SessionExpiredError) throw e;
        return [];
    }
}

/**
 * Obtiene el catálogo de escuelas profesionales registradas.
 */
export async function fetchEscuelas() {
    try {
        const response = await fetch(`${API_URL}/escuelas`, {
            credentials: 'include'
        });
        if (response.status === 401) throw new SessionExpiredError();
        if (!response.ok) return [];
        return await response.json();
    } catch (e) {
        if (e instanceof SessionExpiredError) throw e;
        return [];
    }
}
