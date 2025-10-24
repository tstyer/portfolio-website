/**
 * @jest-environment jsdom
 */

const filterProjects = require('../home');

describe('filterProjects', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="nameSearch" value="app">
      <div data-name="my app"></div>
      <div data-name="website"></div>
    `;

    // match your globals
    global.nameSearch = document.getElementById('nameSearch');
    global.projects = Array.from(document.querySelectorAll('[data-name]'));
  });

  it('shows matches and hides non-matches', () => {
    filterProjects();

    const [matchEl, nonMatchEl] = global.projects;
    expect(matchEl.style.display).toBe('');      // shown
    expect(nonMatchEl.style.display).toBe('none'); // hidden
  });
});