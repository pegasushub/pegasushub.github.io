// =============================================
//  PEGASUSHUB — SHARED SCRIPTS
//  Used by: index.html, pages/academy.html,
//  pages/workflows.html, pages/build.html,
//  pages/ai-tools.html
// =============================================

// --- THEME TOGGLE ---
function toggleTheme() {
    const body = document.body;
    const icon = document.querySelector('.theme-toggle i');
    body.classList.toggle('light-mode');
    if (body.classList.contains('light-mode')) {
        localStorage.setItem('theme', 'light');
        if (icon) { icon.classList.remove('fa-moon'); icon.classList.add('fa-sun'); }
    } else {
        localStorage.setItem('theme', 'dark');
        if (icon) { icon.classList.remove('fa-sun'); icon.classList.add('fa-moon'); }
    }
}

(function initTheme() {
    const saved = localStorage.getItem('theme');
    const icon = document.querySelector('.theme-toggle i');
    if (saved !== 'dark') {
        document.body.classList.add('light-mode');
        if (icon) { icon.classList.remove('fa-moon'); icon.classList.add('fa-sun'); }
    }
})();

// --- BACK TO TOP ---
window.addEventListener('scroll', () => {
    const btn = document.getElementById('back-top');
    if (btn) btn.classList.toggle('visible', window.scrollY > 400);
});
