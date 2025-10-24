

function filterProjects(nameSearchEl, projectEls) {
  const nameQuery = (nameSearchEl.value || '').toLowerCase();

  projectEls.forEach((project) => {
    const name = (project.getAttribute('data-name') || '');
    project.style.display = name.includes(nameQuery) ? '' : 'none';
  });
}

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    const nameSearch = document.getElementById('name-search');
    const projects = document.querySelectorAll('.project');
    // wire up in the browser
    nameSearch.addEventListener('input', () => filterProjects(nameSearch, projects));
  });
}

module.exports = { filterProjects };
