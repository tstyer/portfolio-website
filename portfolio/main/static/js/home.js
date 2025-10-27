const nameSearch = document.getElementById("name-search");
const projects = document.querySelectorAll(".project");
const tags = document.querySelectorAll(".tag");

function filterProjects(nameSearchEl, projectEls) {
  const nameQuery = (nameSearchEl?.value || "").toLowerCase();
  projectEls.forEach((project) => {
    const name = (project.getAttribute("data-name") || "").toLowerCase();
    project.style.display = name.includes(nameQuery) ? "" : "none";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (nameSearch && projects.length) {
    nameSearch.addEventListener("input", () => filterProjects(nameSearch, projects));
    nameSearch.addEventListener("keyup", () => filterProjects(nameSearch, projects));
  }

  if (tags.length && projects.length) {
    tags.forEach((tag) => {
      tag.addEventListener("click", function () {
        const selectedTag = this.getAttribute("data-tag") || "";
        projects.forEach((project) => {
          const projectTags = (project.getAttribute("data-tags") || "").toLowerCase();
          project.style.display = projectTags.includes(selectedTag.toLowerCase()) ? "" : "none";
        });
      });
    });
  }
});

// Export for tests if needed
if (typeof module !== "undefined" && module.exports) {
  module.exports = { filterProjects };
} else {
  window.filterProjects = filterProjects;
}
