document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.getElementById('menu-icon');
    const navLinks = document.getElementById('nav-links');

    // Dropdown menu handler
    menuIcon.addEventListener('click', function() {
        if (navLinks.style.display === 'block') {
            navLinks.style.display = 'none'; // Close menu
        } else {
            navLinks.style.display = 'block'; // Open dropdown menu
        }
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth > 650) {
            navLinks.style.display = 'flex'; // Show the horizontal nav
        } else {
            navLinks.style.display = 'none'; // Hide the dropdown when returning to mobile
        }
    });
});
