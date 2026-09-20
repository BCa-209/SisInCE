import { initTheme } from './theme.js';
import { API_URL } from './config.js';
import { fetchEstudiantes, fetchFacultades, fetchEscuelas } from './api.js';
import { setStudents } from './pagination.js';
import { hideTemplate } from './ui.js';

document.addEventListener('DOMContentLoaded', () => {
    // 1. Iniciar el modo oscuro y cargar SVGs
    initTheme();
    loadCatalogs();

    // 2. Referencias del DOM
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

    // 3. Manejo del Criterio de Búsqueda
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
                
                // Hide all inputs first
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

    // 4. Manejo del Submit del Formulario
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
            resultsContainer.innerHTML = `<p class="alert alert-error">${error.message}</p>`;
            document.getElementById('pagination-container').innerHTML = '';
            
            const resultsCountEl = document.getElementById('results-count');
            if (resultsCountEl) {
                resultsCountEl.textContent = '0';
                resultsCountEl.classList.remove('hidden');
            }
        }
    });

    // 5. Manejo del Botón de Imprimir a PDF
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
    const dataFacultades = await fetchFacultades();
    const dataEscuelas = await fetchEscuelas();

    populateSelects(dataFacultades, dataEscuelas);
}

function populateSelects(facultades, escuelas) {
    const facSelects = [document.getElementById('search-select-facultad'), document.getElementById('custom-facultad')];
    const escSelects = [document.getElementById('search-select-escuela'), document.getElementById('custom-escuela')];

    facSelects.forEach(sel => {
        sel.innerHTML = '<option value="">Todas / Seleccione...</option>';
        facultades.forEach(f => {
            const opt = document.createElement('option');
            opt.value = f.nombre;
            opt.textContent = f.nombre;
            sel.appendChild(opt);
        });
    });

    escSelects.forEach(sel => {
        sel.innerHTML = '<option value="">Todas / Seleccione...</option>';
        escuelas.forEach(e => {
            const opt = document.createElement('option');
            opt.value = e.nombre;
            opt.textContent = e.nombre;
            sel.appendChild(opt);
        });
    });
}
