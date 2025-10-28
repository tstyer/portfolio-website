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

// Functions will hide projects when page loads
function hideAll() {
  projects.forEach((p) => (p.style.display = "none"));
}

function clearActiveTags() {
  document.querySelectorAll(".tag.active").forEach((t) => t.classList.remove("active"));
}

function filterByTag(tag) {
  const t = (tag || "").toLowerCase();
  projects.forEach((project) => {
    const projectTags = (project.getAttribute("data-tags") || "").toLowerCase();
    project.style.display = projectTags.includes(t) ? "" : "none";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // 1) Start hidden
  hideAll();

  // 2) Typing: clear active tag(s) and use the tested function
  if (nameSearch) {
    nameSearch.addEventListener("input", () => {
      clearActiveTags();
      filterProjects(nameSearch, projects);
      // If the box is empty, keep everything hidden
      if (!nameSearch.value.trim()) hideAll();
    });
  }

  // 3) Tag clicks: set active, clear search, filter by tag
  if (tags.length) {
    tags.forEach((tagBtn) => {
      tagBtn.addEventListener("click", function () {
        clearActiveTags();
        this.classList.add("active");
        if (nameSearch) nameSearch.value = ""; // ensure tag filter is applied
        filterByTag(this.dataset.tag || "");
      });
    });
  }
});

// Export for test
if (typeof module !== "undefined" && module.exports) {
  module.exports = { filterProjects, hideAll, filterByTag };
} else {
  window.filterProjects = filterProjects;
}
