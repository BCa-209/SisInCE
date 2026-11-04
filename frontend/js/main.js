import { initTheme } from './theme.js';
import { API_URL } from './config.js';
import { 
    fetchEstudiantes, 
    fetchFacultades, 
    fetchEscuelas, 
    login, 
    logout, 
    fetchCurrentUser, 
    SessionExpiredError 
} from './api.js';
import { setStudents } from './pagination.js';
import { hideTemplate } from './ui.js';

let currentUser = null;

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Iniciar el tema oscuro/claro
    initTheme();

    // 2. Referencias del DOM - Autenticación y Sesión
    const loginSection = document.getElementById('login-section');
    const loginForm = document.getElementById('login-form');
    const loginNombres = document.getElementById('login-nombres');
    const loginApellidos = document.getElementById('login-apellidos');
    const loginCodigo = document.getElementById('login-codigo');
    const loginError = document.getElementById('login-error');
    const loginLoading = document.getElementById('login-loading');
    const btnLoginSubmit = document.getElementById('btn-login-submit');

    const appContent = document.getElementById('app-content');
    const userSessionBar = document.getElementById('user-session-bar');
    const userDisplayName = document.getElementById('user-display-name');
    const btnLogout = document.getElementById('btn-logout');

    // 3. Referencias del DOM - Búsqueda y Resultados
    const form = document.getElementById('search-form');
    const criterioInput = document.getElementById('criterio');
    const criterionBtns = document.querySelectorAll('.criterion-btn');
    const dynamicLabel = document.getElementById('dynamic-label');
    const searchInput = document.getElementById('search-input');
    const searchSelectFacultad = document.getElementById('search-select-facultad');
    const searchSelectEscuela = document.getElementById('search-select-escuela');
    const resultsContainer = document.getElementById('results-container');
    const searchInputSection = document.getElementById('search-input-section');
    const singleFieldWrapper = document.getElementById('single-field-wrapper');
    const customFieldsWrapper = document.getElementById('custom-fields-wrapper');
    const btnPrint = document.getElementById('btn-print');
    const btnCloseTemplate = document.getElementById('btn-close-template');

    // Funciones de control de vista de sesión
    function showLoginView(message = null) {
        currentUser = null;
        appContent.classList.add('hidden');
        userSessionBar.classList.add('hidden');
        loginSection.classList.remove('hidden');

        if (message) {
            loginError.textContent = message;
            loginError.classList.remove('hidden');
        } else {
            loginError.classList.add('hidden');
        }

        // Limpiar contraseña/código por seguridad
        loginCodigo.value = '';
        loginLoading.classList.add('hidden');
        btnLoginSubmit.disabled = false;
    }

    function showAppView(user) {
        currentUser = user;
        loginSection.classList.add('hidden');
        loginError.classList.add('hidden');
        loginLoading.classList.add('hidden');
        btnLoginSubmit.disabled = false;

        const displayName = user.nombres || user.apellidos_nombres || user.codigo;
        userDisplayName.textContent = `${displayName} (${user.codigo})`;
        userDisplayName.title = `${user.apellidos_nombres} - ${user.facultad} - ${user.escuela_profesional}`;
        
        userSessionBar.classList.remove('hidden');
        appContent.classList.remove('hidden');

        // Cargar facultades y escuelas al acceder
        loadCatalogs();
    }

    // 4. Verificación inicial de sesión al cargar la página
    try {
        const user = await fetchCurrentUser();
        if (user) {
            showAppView(user);
        } else {
            showLoginView();
        }
    } catch (err) {
        showLoginView();
    }

    // 5. Manejo del Login con 3 campos (nombres, apellidos, código)
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        loginError.classList.add('hidden');
        loginLoading.classList.remove('hidden');
        btnLoginSubmit.disabled = true;

        const nombres = loginNombres.value.trim();
        const apellidos = loginApellidos.value.trim();
        const codigo = loginCodigo.value.trim();

        try {
            const data = await login(nombres, apellidos, codigo);
            showAppView(data.estudiante);
        } catch (err) {
            loginError.textContent = err.message || 'Error al iniciar sesión';
            loginError.classList.remove('hidden');
        } finally {
            loginLoading.classList.add('hidden');
            btnLoginSubmit.disabled = false;
        }
    });

    // 6. Manejo del Cierre de Sesión (Logout)
    btnLogout.addEventListener('click', async () => {
        await logout();
        showLoginView('Has cerrado sesión correctamente.');
    });

    // Función para limpiar alertas de error al interactuar
    function clearErrorOnInput() {
        const errorAlert = resultsContainer.querySelector('.alert-error');
        if (errorAlert) {
            resultsContainer.innerHTML = '';
            document.getElementById('pagination-container').innerHTML = '';
        }
    }

    // Vincular botón cerrar plantilla
    if (btnCloseTemplate) {
        btnCloseTemplate.addEventListener('click', hideTemplate);
    }
    
    // Limpiar error al tipear o cambiar select
    document.querySelectorAll('.form-control').forEach(el => {
        el.addEventListener('input', clearErrorOnInput);
        el.addEventListener('change', clearErrorOnInput);
    });

    // 7. Manejo del Criterio de Búsqueda
    criterionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            clearErrorOnInput();
            criterionBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const val = btn.dataset.value;
            criterioInput.value = val;
            searchInput.value = '';
            
            searchInputSection.classList.remove('hidden');
            
            if (val === 'personalizada') {
                singleFieldWrapper.classList.add('hidden');
                customFieldsWrapper.classList.remove('hidden');
            } else {
                singleFieldWrapper.classList.remove('hidden');
                customFieldsWrapper.classList.add('hidden');
                
                searchInput.classList.add('hidden');
                searchSelectFacultad.classList.add('hidden');
                searchSelectEscuela.classList.add('hidden');

                switch(val) {
                    case 'codigo':
                        dynamicLabel.textContent = 'Ingrese el Código:';
                        searchInput.type = 'text';
                        searchInput.placeholder = 'Ej. 20240001';
                        searchInput.classList.remove('hidden');
                        break;
                    case 'dni':
                        dynamicLabel.textContent = 'Ingrese el DNI:';
                        searchInput.type = 'text';
                        searchInput.placeholder = 'Ej. 12345678';
                        searchInput.classList.remove('hidden');
                        break;
                    case 'nombre':
                        dynamicLabel.textContent = 'Ingrese Apellidos o Nombres:';
                        searchInput.type = 'text';
                        searchInput.placeholder = 'Ej. Perez';
                        searchInput.classList.remove('hidden');
                        break;
                    case 'facultad':
                        dynamicLabel.textContent = 'Seleccione la Facultad:';
                        searchSelectFacultad.classList.remove('hidden');
                        break;
                    case 'escuela':
                        dynamicLabel.textContent = 'Seleccione la Escuela Profesional:';
                        searchSelectEscuela.classList.remove('hidden');
                        break;
                    case 'ingreso':
                        dynamicLabel.textContent = 'Ingrese el Año de Ingreso:';
                        searchInput.type = 'number';
                        searchInput.placeholder = 'Ej. 2020';
                        searchInput.classList.remove('hidden');
                        break;
                }
            }
        });
    });

    // 8. Manejo del Submit del Formulario de Búsqueda
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const criterio = criterioInput.value;
        let valor = '';
        if (criterio === 'facultad') valor = searchSelectFacultad.value;
        else if (criterio === 'escuela') valor = searchSelectEscuela.value;
        else valor = searchInput.value.trim();
        
        hideTemplate();

        let url = API_URL;
        
        if (criterio === 'personalizada') {
            const params = new URLSearchParams();
            const cCodigo = document.getElementById('custom-codigo').value.trim();
            const cDni = document.getElementById('custom-dni').value.trim();
            const cNombre = document.getElementById('custom-nombre').value.trim();
            const cFacultad = document.getElementById('custom-facultad').value.trim();
            const cEscuela = document.getElementById('custom-escuela').value.trim();
            const cIngreso = document.getElementById('custom-ingreso').value.trim();
            const cCiclo = document.getElementById('custom-ciclo').value.trim();
            const cGenero = document.getElementById('custom-genero').value.trim();
            
            if (cCodigo) params.append('codigo', cCodigo);
            if (cDni) params.append('dni', cDni);
            if (cNombre) params.append('nombre', cNombre);
            if (cFacultad) params.append('facultad', cFacultad);
            if (cEscuela) params.append('escuela', cEscuela);
            if (cIngreso) params.append('ingreso', cIngreso);
            if (cCiclo) params.append('ciclo', cCiclo);
            if (cGenero) params.append('genero', cGenero);
            
            const queryString = params.toString();
            if (queryString) {
                url = `${API_URL}?${queryString}`;
            }
        } else {
            if (valor) {
                if (criterio === 'codigo') url = `${API_URL}/codigo/${valor}`;
                else if (criterio === 'dni') url = `${API_URL}/dni/${valor}`;
                else {
                    url = `${API_URL}?${criterio}=${encodeURIComponent(valor)}`;
                }
            }
        }

        try {
            const estudiantes = await fetchEstudiantes(url);
            setStudents(estudiantes);
        } catch (error) {
            if (error instanceof SessionExpiredError) {
                showLoginView('Su sesión ha expirado por inactividad. Por favor ingrese nuevamente.');
                return;
            }
            resultsContainer.innerHTML = `<p class="alert alert-error">${error.message}</p>`;
            document.getElementById('pagination-container').innerHTML = '';
            
            const resultsCountEl = document.getElementById('results-count');
            if (resultsCountEl) {
                resultsCountEl.textContent = '0';
                resultsCountEl.classList.remove('hidden');
            }
        }
    });

    // 9. Manejo del Botón de Imprimir a PDF
    btnPrint.addEventListener('click', () => {
        const element = document.getElementById('template-canvas');
        
        const opt = {
            margin:       0,
            filename:     `Estudiante_${document.getElementById('t-codigo').textContent}.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2 },
            jsPDF:        { unit: 'mm', format: 'a4', orientation: 'landscape' }
        };

        html2pdf().set(opt).from(element).save();
    });
});

async function loadCatalogs() {
    try {
        const dataFacultades = await fetchFacultades();
        const dataEscuelas = await fetchEscuelas();
        populateSelects(dataFacultades, dataEscuelas);
    } catch (e) {
        console.warn('No se pudieron cargar los catálogos:', e);
    }
}

function populateSelects(facultades, escuelas) {
    const facSelects = [document.getElementById('search-select-facultad'), document.getElementById('custom-facultad')];
    const escSelects = [document.getElementById('search-select-escuela'), document.getElementById('custom-escuela')];

    facSelects.forEach(sel => {
        if (!sel) return;
        sel.innerHTML = '<option value="">Todas / Seleccione...</option>';
        facultades.forEach(f => {
            const opt = document.createElement('option');
            opt.value = f.nombre;
            opt.textContent = f.nombre;
            sel.appendChild(opt);
        });
    });

    escSelects.forEach(sel => {
        if (!sel) return;
        sel.innerHTML = '<option value="">Todas / Seleccione...</option>';
        escuelas.forEach(e => {
            const opt = document.createElement('option');
            opt.value = e.nombre;
            opt.textContent = e.nombre;
            sel.appendChild(opt);
        });
    });
}
