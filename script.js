const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');
const menuIconOpen = document.getElementById('menu-icon-open');
const menuIconClose = document.getElementById('menu-icon-close');

mobileMenuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
    const isHidden = mobileMenu.classList.contains('hidden');

    if (isHidden) {
        // Menu is closed, show hamburger icon
        menuIconOpen.classList.remove('opacity-0');
        menuIconClose.classList.add('opacity-0');
    } else {
        // Menu is open, show close icon
        menuIconOpen.classList.add('opacity-0');
        menuIconClose.classList.remove('opacity-0');
    }
});

// Close the mobile menu when a link is clicked
const mobileLinks = mobileMenu.querySelectorAll('a');
mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        menuIconOpen.classList.remove('opacity-0');
        menuIconClose.classList.add('opacity-0');
    });
});

// Close the mobile menu on window resize if screen becomes desktop size
window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
        mobileMenu.classList.add('hidden');
        menuIconOpen.classList.remove('opacity-0');
        menuIconClose.classList.add('opacity-0');
    }
});