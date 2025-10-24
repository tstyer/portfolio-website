

document.addEventListener("DOMContentLoaded", function() {
    const nameSearch = document.getElementById("name-search")
    const tags = document.querySelectorAll(".tag")
    const projects = document.querySelectorAll(".project")

    function filterProjects() {
        const nameQuery = nameSearch.value.toLowerCase();

        projects.forEach((project) => {
            const name = project.getAttribute('data-name')
            const nameMatch = name.includes(nameQuery)

            if (nameMatch) {
                project.style.display = "";
            } else {
                project.style.display = "none";
            }
        })
    }

})

module.exports = {filterProjects};
