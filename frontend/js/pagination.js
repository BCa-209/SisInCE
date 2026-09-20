import { ITEMS_PER_PAGE } from './config.js';
import { renderPageItems } from './ui.js';

export let allStudents = [];
export let currentPage = 1;

export function setStudents(estudiantes) {
    allStudents = estudiantes;
    currentPage = 1;
    
    const resultsCountEl = document.getElementById('results-count');
    if (resultsCountEl) {
        resultsCountEl.textContent = allStudents.length;
        resultsCountEl.classList.remove('hidden');
    }

    renderPage(1);
}

export function renderPage(page) {
    const startIndex = (page - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const pageStudents = allStudents.slice(startIndex, endIndex);
    
    renderPageItems(pageStudents);
    renderPaginationControls();
}

function renderPaginationControls() {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = '';
    
    const totalPages = Math.ceil(allStudents.length / ITEMS_PER_PAGE);
    if (totalPages <= 1) return;

    const createBtn = (text, pageToLoad, isCurrent) => {
        const btn = document.createElement('button');
        btn.textContent = text;
        if (text === '...') {
            btn.disabled = true;
            btn.className = 'btn-secondary';
            btn.style.opacity = '0.5';
            btn.style.cursor = 'default';
        } else {
            btn.className = isCurrent ? 'btn-primary' : 'btn-secondary';
            btn.addEventListener('click', () => {
                currentPage = pageToLoad;
                renderPage(pageToLoad);
            });
        }
        btn.style.padding = '5px 10px';
        return btn;
    };

    let pages = [];
    if (totalPages <= 5) {
        for (let i = 1; i <= totalPages; i++) pages.push(i);
    } else {
        if (currentPage <= 3) {
            pages = [1, 2, 3, 4, '...', totalPages];
        } else if (currentPage >= totalPages - 2) {
            pages = [1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages];
        } else {
            pages = [1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages];
        }
    }

    pages.forEach(p => {
        paginationContainer.appendChild(createBtn(p, p !== '...' ? p : null, p === currentPage));
    });
}
