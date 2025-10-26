const nameSearch = document.getElementById("name-search");
const projects = document.querySelectorAll(".project");
const tags = document.querySelectorAll(".tag");

function filterProjects(nameSearchEl, projectEls) {
  const nameQuery = (nameSearchEl.value || "").toLowerCase();

  // Loop through all the projects to see if the query is in the project name.
  projectEls.forEach((project) => {
    const name = project.getAttribute("data-name") || ""; // Self-learn note: I get the data name attribute.
    project.style.display = name.includes(nameQuery) ? "" : "none"; // If it includes the name, the display doesn't change, otherwise, shows 'none'.
  });
}

if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", () => {
    // wire up in the browser
    nameSearch.addEventListener("input", () =>
      filterProjects(nameSearch, projects)
    );
  });

  // The below function will filter based on tags clicked.
  tags.forEach((tag) => {
        tag.addEventListener("click", function () {
            const selectedTag = this.getAttribute("data-tag")

            projects.forEach((project) => {
                const projectTags = project.getAttribute("data-tags")
                if (projectTags.includes(selectedTag)) {
                    project.style.display = ""
                } else {
                    project.style.display = "none"
                }
            })
        })
    })

  nameSearch.addEventListener("keyup", filterProjects)
}

// Make available to Jest (Node) but don't crash in the browser.
if (typeof module !== "undefined" && module.exports) {
  module.exports = { filterProjects };
} else {
  window.filterProjects = filterProjects;
}
