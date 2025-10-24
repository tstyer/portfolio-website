

function filterProjects(nameSearchEl, projectEls) {
  const nameQuery = (nameSearchEl.value || '').toLowerCase();

  // Loop through all the projects to see if the query is in the project name. 
  projectEls.forEach((project) => {
    const name = (project.getAttribute('data-name') || ''); // Self-learn note: I get the data name attribute. 
    project.style.display = name.includes(nameQuery) ? '' : 'none'; // If it includes the name, the display doesn't change, otherwise, shows 'none'.
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
