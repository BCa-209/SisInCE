import { API_URL } from './config.js';

export async function fetchEstudiantes(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error('No se encontraron resultados');
    const data = await response.json();
    return Array.isArray(data) ? data : [data];
}

export async function fetchFacultades() {
    const baseUrl = API_URL.replace('/api/estudiantes', '/api/estudiantes/facultades'); // Simple approach
    // actually API_URL is 'http://localhost:8000/api/estudiantes'
    // The route we added is router.get("/facultades"), which has prefix="/api/estudiantes"
    const response = await fetch(`${API_URL}/facultades`);
    if (!response.ok) return [];
    return await response.json();
}

export async function fetchEscuelas() {
    const response = await fetch(`${API_URL}/escuelas`);
    if (!response.ok) return [];
    return await response.json();
}