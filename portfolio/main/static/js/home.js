const nameSearch = document.getElementById("name-search");
const projects = document.querySelectorAll(".project");
const tags = document.querySelectorAll(".tag");

function toggleInfoParagraph() {
  const info = document.getElementById("temp-p");
  // count how many projects are currently visible
  let visibleCount = 0;
  projects.forEach(p => {
    if (p.style.display !== "none") {
      visibleCount++;
    }
  });

  if (visibleCount > 0) {
    info.classList.add("hidden");
  } else {
    info.classList.remove("hidden");
  }
}

function filterProjects(nameSearchEl, projectEls) {
  const nameQuery = (nameSearchEl?.value || "").toLowerCase();
  let visibleProjects = [];

  projectEls.forEach((project) => {
    const name = (project.getAttribute("data-name") || "").toLowerCase();
    const match = name.includes(nameQuery);

    if (match) {
      project.style.display = "";
      visibleProjects.push(project);    // collect only visible projects
    } else {
      project.style.display = "none";
      project.classList.remove("fade-in-up"); // no matches = remove the css class
    }
  });

  // show/hide info paragraph
  const info = document.getElementById("temp-p");
  if (info) {
    if (visibleProjects.length > 0) {
      info.classList.add("hidden");
    } else {
      info.classList.remove("hidden");
    }
  }

  // now animate the visible ones
  visibleProjects.forEach((project, index) => {
    // remove first so re-adding re-triggers animation
    project.classList.remove("fade-in-up");

    // small timeout, then add class
    setTimeout(() => {
      project.classList.add("fade-in-up");
      // stagger each item delayed by 100ms
      project.style.animationDelay = `${index * 100}ms`;
    }, 0);
  });
}


// Functions will hide projects when page loads
function hideAll() {
  projects.forEach((p) => {
    p.style.display = "none";
    p.classList.remove("fade-in-up");
    p.style.animationDelay = "0ms";
  });
  toggleInfoParagraph();
}


function clearActiveTags() {
  document.querySelectorAll(".tag.active").forEach((t) => t.classList.remove("active"));
}

function filterByTag(tag) {
  const t = (tag || "").toLowerCase();
  let visibleProjects = [];

  projects.forEach((project) => {
    const projectTags = (project.getAttribute("data-tags") || "").toLowerCase();
    const match = projectTags.includes(t);

    if (match) {
      project.style.display = "";
      visibleProjects.push(project);
    } else {
      project.style.display = "none";
      project.classList.remove("fade-in-up");
    }
  });

  const info = document.getElementById("temp-p");
  if (info) {
    if (visibleProjects.length > 0) {
      info.classList.add("hidden");
    } else {
      info.classList.remove("hidden");
    }
  }

  // staggered wave again
  visibleProjects.forEach((project, index) => {
    project.classList.remove("fade-in-up");
    setTimeout(() => {
      project.classList.add("fade-in-up");
      project.style.animationDelay = `${index * 150}ms`;
    }, 0);
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

// Navigation bar collapse
const btn = document.querySelector('.nav-toggle');
const menu = document.querySelector('.nav-menu');

if (btn && menu) {
  btn.addEventListener('click', () => {
    menu.classList.toggle('is-open');
  });
}

// Export for test
if (typeof module !== "undefined" && module.exports) {
  module.exports = { filterProjects, hideAll, filterByTag };
} else {
  window.filterProjects = filterProjects;
}
