function insertNav() {
    nav = `
    <span>
        <!-- Navbar -->
        <!-- <nav class="bg-white dark:bg-neutral-800 shadow-md shadow-neutral-300 p-4 sticky top-0 z-50 transition-colors duration-300 dark:shadow-neutral-700"> -->
        <nav class="border-b border-neutral-700 border-neutral p-4 sticky top-0 z-50 transition-colors duration-300 dark bg-gray-50 dark:bg-gray-950">
            <div class="container mx-auto flex justify-between items-center">
                <!-- Logo -->
                <a href="../" class="flex items-center space-x-2">
                    <!-- <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500 dark:text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                    </svg> -->
                    <img src="https://kmu.pisc.cc/img/logo-nobg.png" alt="EP" sizes="100vw" class="w-8 h-8">
                    <span class="text-xl font-bold text-neutral-800 dark:text-white">E15</span>
                </a>

                <!-- Mobile Menu Button -->
                <div class="md:hidden">
                    <button id="mobile-menu-button" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-300 focus:outline-none focus:ring-2 focus:ring-neutral-300 rounded-md p-2 transition-transform duration-300 hover:bg-neutral-200 dark:hover:bg-neutral-700 shadow-lg">
                        <svg class="w-6 h-6 transform transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path id="menu-icon-open" class="transition-opacity duration-300" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 6h16M4 12h16m-7 6h7"></path>
                            <path id="menu-icon-close" class="opacity-0 transition-opacity duration-300" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>

                <!-- Desktop Navigation Links -->
                <!-- <div class="hidden md:space-x-8 md:flex flex items-center justify-center space-x-4 font-medium transition-colors">
                    <a href="../" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Home</a>
                    <a href="../schedule" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Class Schedule</a>
                    <a href="../old-exam" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Old Exam</a>
                </div> -->
                <div class="hidden md:space-x-8 md:flex flex items-center justify-center space-x-4 font-medium transition-colors">
                    <a href="https://kmu.pisc.cc/" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Home</a>
                    <a href="https://kmu.pisc.cc/schedule" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Class Schedule</a>
                    <a href="https://kmu.pisc.cc/old-exam" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Old Exam</a>
                </div>
            </div>
        </nav>

        <!-- Mobile Menu -->
        <div id="mobile-menu" class="hidden md:hidden shadow-md rounded-md m-4 transition-all duration-300 ease-in-out bg-neutral-100 dark:bg-neutral-800">
            <div class="p-4 flex flex-col space-y-2
            [&>*]
            ">
                <a href="../" class="bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 font-medium transition-colors duration-300 rounded-md py-2 px-3">Home</a>
                <a href="../schedule" class="bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 font-medium transition-colors duration-300 rounded-md py-2 px-3">Class Schedule</a>
                <a href="../old-exam" class="bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 font-medium transition-colors duration-300 rounded-md py-2 px-3">Old Exam</a>
            </div>
        </div>
    <span>
    `
// a
//                     <a href="../storage" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Storage</a>
//                     <a href="https://kmu.pisc.cc/storage" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Storage</a>
//                 <a href="../storage" class="bg-neutral-200 dark:bg-neutral-700 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 font-medium transition-colors duration-300 rounded-md py-2 px-3">Storage</a>
    const parser = new DOMParser();
    const doc = parser.parseFromString(nav, "text/html");
    const elem = doc.querySelector("span");

    document.body.prepend(elem);
};

// insertNav();

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
        
        // window.scrollTo(0, 1000);
        window.scrollTo({ top: 0, behavior: "smooth" });
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
//     topContent.classList.toggle('hover:bg-neutral-200');
//     topContent.classList.toggle('hover:dark:bg-neutral-700');
//     topContent.classList.toggle('bg-neutral-200');
//     topContent.classList.toggle('dark:bg-neutral-700');
//     const expandedContent = element.parentElement.parentElement.querySelector('.content-expanded');
//     expandedContent.classList.toggle('hidden');
// }

function toggleContent(element) {
    element.querySelector('.expand-button').classList.toggle('rotate-180');
    const topContent = element.querySelector('.top-content');
    topContent.classList.toggle('rounded-t-md');
    topContent.classList.toggle('rounded-md');
    topContent.classList.toggle('hover:bg-neutral-200');
    topContent.classList.toggle('hover:dark:bg-neutral-700');
    topContent.classList.toggle('bg-neutral-200');
    topContent.classList.toggle('dark:bg-neutral-700');
    const expandedContent = element.parentElement.querySelector('.content-expanded');
    expandedContent.classList.toggle('hidden');
}

function createClockForm() {
    const clockFormHtml = `
    <div>
        <form id="clock-form" action="../clock" method="get">
            <button id="clock-page-button" class="bg-white dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 border border-neutral-200 dark:border-neutral-700 shadow-md w-12 h-12 rounded-lg flex items-center justify-center p-2 bottom-4 right-4 fixed">
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

createClockForm();

document.body.setAttribute('class', '');
// $('body').removeClass();
document.body.classList.add("dark", "bg-gray-50", "dark:bg-gray-950", "min-h-screen")