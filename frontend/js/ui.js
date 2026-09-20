let selectedStudent = null;

export function renderPageItems(pageStudents) {
    const resultsContainer = document.getElementById('results-container');
    const template = document.getElementById('student-card-template');
    
    resultsContainer.innerHTML = '';
    
    pageStudents.forEach(est => {
        const clone = template.content.cloneNode(true);
        
        clone.querySelector('.student-name').textContent = est.apellidos_nombres;
        clone.querySelector('.student-code').textContent = est.codigo;
        clone.querySelector('.student-dni').textContent = est.dni;
        clone.querySelector('.student-faculty').textContent = est.facultad;
        clone.querySelector('.student-school').textContent = est.escuela_profesional;
        
        const btnCopy = clone.querySelector('.btn-copy');
        btnCopy.addEventListener('click', () => {
            const textToCopy = `Código: ${est.codigo}\nDNI: ${est.dni}\nApellidos y Nombres: ${est.apellidos_nombres}\nFacultad: ${est.facultad}\nEscuela Profesional: ${est.escuela_profesional}`;
            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = btnCopy.textContent;
                btnCopy.textContent = '¡Copiado!';
                setTimeout(() => btnCopy.textContent = originalText, 2000);
            });
        });

        const btnSelect = clone.querySelector('.btn-select');
        btnSelect.addEventListener('click', () => {
            selectedStudent = est;
            populateTemplate();
        });

        resultsContainer.appendChild(clone);
    });
}

function populateTemplate() {
    if (!selectedStudent) return;
    
    document.getElementById('t-codigo').textContent = selectedStudent.codigo;
    document.getElementById('t-dni').textContent = selectedStudent.dni;
    document.getElementById('t-nombre').textContent = selectedStudent.apellidos_nombres;
    document.getElementById('t-facultad').textContent = selectedStudent.facultad;
    document.getElementById('t-escuela').textContent = selectedStudent.escuela_profesional;
    
    const ingresoStr = selectedStudent.anio_ingreso || "2020";
    const cicloStr = selectedStudent.ciclo ? `Ciclo ${selectedStudent.ciclo}` : "VIII";
    document.getElementById('t-ingreso-ciclo').textContent = `${ingresoStr} - ${cicloStr}`;

    const templateSection = document.getElementById('template-section');
    templateSection.classList.remove('hidden');
    
    // Mejorar heurística 8: Scroll más suave
    setTimeout(() => {
        templateSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 150);
}

export function hideTemplate() {
    const templateSection = document.getElementById('template-section');
    templateSection.classList.add('hidden');
    selectedStudent = null;
}
