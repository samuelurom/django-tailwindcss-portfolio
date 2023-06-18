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

// Get theme toggle button
const themeToggle = document.getElementById('toggle-btn');

themeToggle.addEventListener('click', () => {
    const isDarkTheme = document.documentElement.classList.contains('dark')

    if (isDarkTheme) {
        document.documentElement.classList.remove("dark");
        setLightTheme();
    } else {
        document.documentElement.classList.add("dark");
        setDarkTheme();
    }
});

// Get popover menu modal
const popOverMenu = document.getElementById("popover-menu")
const menuBtn = document.getElementById("menu-btn")
const closeMenuBtn = document.getElementById("close-menu")

// Show mobile menu
menuBtn.addEventListener('click', () => {
    popOverMenu.classList.remove("hidden")
});

// Close mobile menu
closeMenuBtn.addEventListener('click', () => {
    popOverMenu.classList.add("hidden")
})