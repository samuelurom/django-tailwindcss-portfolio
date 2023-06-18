// On page load or when changing themes, best to add inline in `head` to avoid FOUC
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}

// Whenever the user explicitly chooses light mode
function setLightTheme() {
    localStorage.theme = 'light';
}

// Whenever the user explicitly chooses dark mode
function setDarkTheme() {
    localStorage.theme = 'dark';
}

// Whenever the user explicitly chooses to respect the OS preference
function setOsTheme() {
    localStorage.removeItem('theme');
}