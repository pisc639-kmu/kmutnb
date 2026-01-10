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

        window.scrollTo(0, 1000);
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

// function toggleContent(element) {
//     element.classList.toggle('rotate-180');
//     const topContent = element.parentElement;
//     topContent.classList.toggle('rounded-t-md');
//     topContent.classList.toggle('rounded-md');
//     topContent.classList.toggle('hover:bg-gray-200');
//     topContent.classList.toggle('hover:dark:bg-gray-700');
//     topContent.classList.toggle('bg-gray-200');
//     topContent.classList.toggle('dark:bg-gray-700');
//     const expandedContent = element.parentElement.parentElement.querySelector('.content-expanded');
//     expandedContent.classList.toggle('hidden');
// }

function toggleContent(element) {
    element.querySelector('.expand-button').classList.toggle('rotate-180');
    const topContent = element.querySelector('.top-content');
    topContent.classList.toggle('rounded-t-md');
    topContent.classList.toggle('rounded-md');
    topContent.classList.toggle('hover:bg-gray-200');
    topContent.classList.toggle('hover:dark:bg-gray-700');
    topContent.classList.toggle('bg-gray-200');
    topContent.classList.toggle('dark:bg-gray-700');
    const expandedContent = element.parentElement.querySelector('.content-expanded');
    expandedContent.classList.toggle('hidden');
}

function createClockForm() {
    const clockFormHtml = `
    <div>
        <form id="clock-form" action="../clock" method="get">
            <button id="clock-page-button" class="bg-white dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700 shadow-md w-12 h-12 rounded-lg flex items-center justify-center p-2 bottom-4 right-4 fixed">
                <svg class="transform transition-transform duration-300 justify-center" fill="none" stroke="currentColor" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
                    <path
                    id=""
                    class=""
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1"
                    d="M 6 1 A 1 1 0 0 0 6 11 A 1 1 0 0 0 6 1 Z M 6 3 L 6 6 L 8 7"
                    ></path>
                </svg>
            </button>
        </form>
    </div>
    `;

    const parser = new DOMParser();
    const doc = parser.parseFromString(clockFormHtml, 'text/html');
    const clockForm = doc.getElementById('clock-form');
    document.body.appendChild(clockForm);
}

// createClockForm();