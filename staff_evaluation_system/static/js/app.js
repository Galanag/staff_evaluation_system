(function () {
  const root = document.documentElement;
  const themeButtons = document.querySelectorAll('#themeToggle');
  const storedTheme = (() => { try { return localStorage.getItem('au-evaluation-theme'); } catch (_) { return null; } })();
  if (storedTheme === 'dark' || storedTheme === 'light') root.dataset.theme = storedTheme;

  function refreshThemeLabels() {
    const dark = root.dataset.theme === 'dark';
    themeButtons.forEach((button) => {
      const label = button.querySelector('.theme-label');
      const symbol = button.querySelector('.theme-symbol');
      if (label) label.textContent = dark ? 'Light mode' : 'Dark mode';
      if (symbol) symbol.textContent = dark ? '☀' : '◐';
      button.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    });
  }
  themeButtons.forEach((button) => button.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('au-evaluation-theme', root.dataset.theme); } catch (_) { /* Storage can be disabled. */ }
    refreshThemeLabels();
  }));
  refreshThemeLabels();

  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  if (sidebarToggle && sidebar) sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
  document.addEventListener('click', (event) => {
    if (!sidebar || !sidebar.classList.contains('open')) return;
    if (!sidebar.contains(event.target) && sidebarToggle && !sidebarToggle.contains(event.target)) sidebar.classList.remove('open');
  });
  document.querySelectorAll('.alert-close').forEach((button) => button.addEventListener('click', () => {
    const alert = button.closest('.alert');
    if (alert) alert.remove();
  }));

  // The chart is intentionally dependency-free and scales bars to the highest count.
  const barFills = Array.from(document.querySelectorAll('.bar-fill'));
  if (barFills.length) {
    const max = Math.max(1, ...barFills.map((el) => Number(el.dataset.count || 0)));
    barFills.forEach((el) => { el.style.height = `${Math.max(2, Number(el.dataset.count || 0) / max * 100)}%`; });
  }

  // Preview administrative total live in the browser; the server remains authoritative.
  const scoreFields = ['id_plan_execution_score', 'id_employee_score', 'id_team_score', 'id_supervisor_score'];
  const scorePreview = document.getElementById('scorePlanPreview');
  function updateScorePreview() {
    if (!scorePreview) return;
    const sum = scoreFields.reduce((total, id) => {
      const field = document.getElementById(id);
      const value = field ? Number(field.value || 0) : 0;
      return total + (Number.isFinite(value) ? value : 0);
    }, 0);
    scorePreview.textContent = Math.min(100, Math.max(0, sum)).toFixed(2);
  }
  scoreFields.forEach((id) => { const field = document.getElementById(id); if (field) field.addEventListener('input', updateScorePreview); });
  updateScorePreview();

  const staffSelect = document.getElementById('id_staff');
  const staffDataNode = document.getElementById('staff-directory-data');
  let staffDirectory = {};
  if (staffDataNode) {
    try { staffDirectory = JSON.parse(staffDataNode.textContent || '{}'); } catch (_) { staffDirectory = {}; }
  }
  if (staffSelect) {
    const fillStaffDetails = () => {
      const person = staffDirectory[staffSelect.value] || {};
      const titleField = document.getElementById('staffJobTitle');
      const gradeField = document.getElementById('staffGrade');
      const processField = document.getElementById('staffJobProcess');
      const readonlyDepartment = document.getElementById('staffDepartment');
      if (titleField) titleField.value = person.position || '';
      if (gradeField) gradeField.value = person.grade || '';
      if (processField) processField.value = person.job_process || '';
      if (readonlyDepartment) readonlyDepartment.value = person.department || '';
      const collegeField = document.getElementById('id_college');
      const departmentField = document.getElementById('id_department');
      if (collegeField && person.college) collegeField.value = person.college;
      if (departmentField && person.department) departmentField.value = person.department;
    };
    staffSelect.addEventListener('change', fillStaffDetails);
    if (staffSelect.value) fillStaffDetails();
  }
})();
