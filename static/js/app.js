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