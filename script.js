(()=>{
const _w = window;
const _document = document;
const _document_body = _document.body
const _querySelector = (element, selector) => element.querySelector(selector);
// const _querySelectorAll = (element, selector) => element.querySelectorAll(selector);
// const _getElementById = (element, id) => {return element.getElementById(id)};
const _document_querySelector = (selector) => _querySelector(_document, selector);
// const _document_querySelectorAll = (selector) => _querySelectorAll(_document, selector);
// const _document_getElementById = (id) => _getElementById(_document, id);
const _document_createElement = (element) => _document.createElement(element);
const _classList = (element) => element.classList;
const _classList_add = (element, ...className) => _classList(element).add(...className);
const _classList_remove = (element, ...className) => _classList(element).remove(...className);
const _classList_toggle = (element, ...className) => _classList(element).toggle(...className);
const _setAttribute = (element, attribute, value) => element.setAttribute(attribute, value);
const _innerHTML = (element, html) => element.innerHTML = html;
const _appendChild = (element, child) => element.appendChild(child);
const _addEventListener = (element, event, callback) => element.addEventListener(event, callback);

    // function insertNav() {
    //     nav = `
    // <span>
    // <nav class="border-b border-neutral-700 border-neutral p-4 sticky top-0 z-50 transition-colors duration-300 dark bg-gray-50 dark:bg-gray-950">
    // <div class="container mx-auto flex justify-between items-center">
    // <a href="../" class="flex items-center space-x-2"><img src="/img/logo-nobg.png" alt="EP" sizes="100vw" class="w-8 h-8"><span class="text-xl font-bold text-neutral-800 dark:text-white">E15</span></a>
    // <div class="md:hidden"><button id="mobile-menu-button" class="text-neutral-500 dark:text-neutral-400 hover:text-neutral-700 dark:hover:text-neutral-300 focus:outline-none focus:ring-2 focus:ring-neutral-300 rounded-md p-2 transition-transform duration-300 hover:bg-neutral-200 dark:hover:bg-neutral-700 shadow-lg"><svg class="w-6 h-6 transform transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path id="menu-icon-open" class="transition-opacity duration-300" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 6h16M4 12h16m-7 6h7"></path><path id="menu-icon-close" class="opacity-0 transition-opacity duration-300" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M6 18L18 6M6 6l12 12"></path></svg></button></div>
    // <div class="hidden md:space-x-8 md:flex flex items-center justify-center space-x-4 font-medium transition-colors">
    // <a href="/" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Home</a>
    // <a href="/schedule" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Class Schedule</a>
    // <a href="/old-exam" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Old Exam</a>
    // </div>
    // </div>
    // </nav>
    // <div id="mobile-menu" class="hidden md:hidden shadow-md rounded-md m-4 transition-all duration-300 ease-in-out bg-neutral-100 dark:bg-neutral-800">
    // <div class="p-4 flex flex-col space-y-2 [&>*] ">
    // <a href="../" class="bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 font-medium transition-colors duration-300 rounded-md py-2 px-3">Home</a>
    // <a href="../schedule" class="bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 font-medium transition-colors duration-300 rounded-md py-2 px-3">Class Schedule</a>
    // <a href="../old-exam" class="bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 font-medium transition-colors duration-300 rounded-md py-2 px-3">Old Exam</a>
    // </div>
    // </div>
    // <span>
    //     `
    // // a
    // //                     <a href="../storage" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Storage</a>
    // //                     <a href="/storage" class="text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 duration-300 rounded-md py-2 px-3 hover:bg-neutral-200 dark:hover:bg-neutral-700">Storage</a>
    // //                 <a href="../storage" class="bg-neutral-200 dark:bg-neutral-700 hover:bg-neutral-300 dark:hover:bg-neutral-600 text-neutral-600 dark:text-neutral-300 hover:text-blue-500 dark:hover:text-blue-400 font-medium transition-colors duration-300 rounded-md py-2 px-3">Storage</a>
    //     const parser = new DOMParser();
    //     const doc = parser.parseFromString(nav, "text/html");
    //     const elem = doc.querySelector("span");

    //     d.body.prepend(elem);
    // };

    // // insertNav();

const mobileMenuButton = _document_querySelector('#mobile-menu-button');
const mobileMenu = _document_querySelector('#mobile-menu');
const menuIconOpen = _document_querySelector('#menu-icon-open');
const menuIconClose = _document_querySelector('#menu-icon-close');

_addEventListener(mobileMenuButton, 'click', () => {
    _classList_toggle(mobileMenu, 'hidden');
    const isHidden = _classList(mobileMenu).contains('hidden');

    if (isHidden) {
        // Menu is closed, show hamburger icon
        _classList_remove(menuIconOpen, 'opacity-0');
        _classList_add(menuIconClose, 'opacity-0');
        
    } else {
        // Menu is open, show close icon
        _classList_add(menuIconOpen, 'opacity-0');
        _classList_remove(menuIconClose, 'opacity-0');
        
        // _w.scrollTo(0, 1000);
        _w.scrollTo({ top: 0, behavior: "smooth" });
    }
});

// Close the mobile menu when a link is clicked
const mobileLinks = mobileMenu.querySelectorAll('a');
mobileLinks.forEach(link => {
    _addEventListener(link, 'click', () => {
        _classList_add(mobileMenu, 'hidden');
        _classList_remove(menuIconOpen, 'opacity-0');
        _classList_add(menuIconClose, 'opacity-0');
    });
});

// Close the mobile menu on _w resize if screen becomes desktop size
_addEventListener(_w, 'resize', () => {
    if (_w.innerWidth >= 768) {
        _classList_add(mobileMenu, 'hidden');
        _classList_remove(menuIconOpen, 'opacity-0');
        _classList_add(menuIconClose, 'opacity-0');
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

// function toggleContent(element) {
//     _classList_toggle(_document_querySelector(element, '.expand-button'), 'rotate-180');
//     const topContent = element.querySelector('.top-content');
//     // topContent.classList.toggle('rounded-t-md');
//     // topContent.classList.toggle('rounded-md');
//     // topContent.classList.toggle('hover:bg-neutral-200');
//     // topContent.classList.toggle('hover:dark:bg-neutral-700');
//     // topContent.classList.toggle('bg-neutral-200');
//     // topContent.classList.toggle('dark:bg-neutral-700');
//     ['rounded-t-md', 'rounded-md', 'hover:bg-neutral-200', 'hover:dark:bg-neutral-700', 'bg-neutral-200', 'dark:bg-neutral-700'].forEach(a => _classList_toggle(topContent, a));
//     const expandedContent = _querySelector(element.parentElement, '.content-expanded');
//     _classList_toggle(expandedContent, 'hidden');
// }

// function clockFormDiv() {
//     const div = _document_createElement('div');
//     const form = _document_createElement('form');
//     form.id = 'clock-form';
//     form.action = '/clock';
//     form.method = 'get';
//     _innerHTML(div,form);

//     const button = _document_createElement('button');
//     button.id = 'clock-page-button';
//     _classList_add(button, 'bg-white', 'dark:bg-neutral-800', 'hover:bg-neutral-200', 'dark:hover:bg-neutral-700', 'border', 'border-neutral-200', 'dark:border-neutral-700', 'shadow-md', 'w-12', 'h-12', 'rounded-lg', 'flex', 'items-center', 'justify-center', 'p-2');

//     const svg = _document_createElement("http://www.w3.org/2000/svg", "svg");
//     // svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
//     // svg.setAttribute("viewBox", "0 0 24 24");
//     // svg.setAttribute("fill", "none");
//     // svg.setAttribute("stroke", "currentColor");
//     // svg.setAttribute("stroke-width", "2");
//     // svg.setAttribute("stroke-linecap", "round");
//     // svg.setAttribute("stroke-linejoin", "round");
//     _setAttribute(svg, "xmlns", "http://www.w3.org/2000/svg");
//     _setAttribute(svg, "viewBox", "0 0 24 24");
//     _setAttribute(svg, "fill", "none");
//     _setAttribute(svg, "stroke", "currentColor");
//     _setAttribute(svg, "stroke-width", "2");
//     _setAttribute(svg, "stroke-linecap", "round");
//     _setAttribute(svg, "stroke-linejoin", "round");
//     // svg.classList.add('w-6', 'h-6');
//     _classList_add(svg, 'w-6', 'h-6');
//     // svg.innerHTML = '<path d="M19 9l-7 7-7-7"/>';
//     _innerHTML(svg, '<path d="M19 9l-7 7-7-7"/>');

//     _appendChild(button, svg);
//     _appendChild(form, button);
    
//     return div;
// }

function createClockForm() {
    // const clockFormHtml = `
    // <div>
    //     <form id="clock-form" action="../clock" emthod="get">
    //         <button id="clock-page-button" class="bg-white dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 border border-neutral-200 dark:border-neutral-700 shadow-md w-12 h-12 rounded-lg flex items-center justify-center p-2 bottom-4 right-4 fixed">
    //             <svg class="transform transition-transform duration-300 justify-center" fill="none" stroke="currentColor" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
    //                 <path
    //                 id=""
    //                 class=""
    //                 stroke-linecap="round"
    //                 stroke-linejoin="round"
    //                 stroke-width="1"
    //                 d="M 6 1 A 1 1 0 0 0 6 11 A 1 1 0 0 0 6 1 Z M 6 3 L 6 6 L 8 7"
    //                 ></path>
    //             </svg>
    //         </button>
    //     </form>
    // </div>
    // `;

    
    const clockFormHtml = '<div><form id="clock-form" action="../clock" emthod="get"><button id="clock-page-button" class="bg-white dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 border border-neutral-200 dark:border-neutral-700 shadow-md w-12 h-12 rounded-lg flex items-center justify-center p-2 bottom-4 right-4 fixed"><svg class="transform transition-transform duration-300 justify-center" fill="none" stroke="currentColor" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg"><path id="" class="" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M 6 1 A 1 1 0 0 0 6 11 A 1 1 0 0 0 6 1 Z M 6 3 L 6 6 L 8 7"></path></svg></button></form></div>';

    // const clockFormHtml = clockFormDiv();

    const parser = new DOMParser();
    const doc = parser.parseFromString(clockFormHtml, 'text/html');
    const clockForm = _querySelector(doc, '#clock-form');
    _appendChild(_document_body, clockForm);
}

createClockForm();

_setAttribute(_document_body, 'class', '');
// $('body').removeClass();
_classList_add(_document_body, "dark", "bg-gray-50", "dark:bg-gray-950", "min-h-screen")
})();