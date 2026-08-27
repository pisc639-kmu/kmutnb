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
const menuIcon = _document_querySelector('#menu-icon');

// _addEventListener(mobileMenuButton, 'click', () => {
//     _classList_toggle(mobileMenu, 'hidden');
//     const isHidden = _classList(mobileMenu).contains('hidden');

//     if (isHidden) {
//         // Menu is closed, show hamburger icon
//         _classList_remove(menuIconOpen, 'opacity-0');
//         _classList_add(menuIconClose, 'opacity-0');
        
//     } else {
//         // Menu is open, show close icon
//         _classList_add(menuIconOpen, 'opacity-0');
//         _classList_remove(menuIconClose, 'opacity-0');
        
//         // _w.scrollTo(0, 1000);
//         _w.scrollTo({ top: 0, behavior: "smooth" });
//     }
// });

// // Close the mobile menu when a link is clicked
// const mobileLinks = mobileMenu.querySelectorAll('a');
// mobileLinks.forEach(link => {
//     _addEventListener(link, 'click', () => {
//         _classList_add(mobileMenu, 'hidden');
//         _classList_remove(menuIconOpen, 'opacity-0');
//         _classList_add(menuIconClose, 'opacity-0');
//     });
// });

// // Close the mobile menu on _w resize if screen becomes desktop size
// _addEventListener(_w, 'resize', () => {
//     if (_w.innerWidth >= 768) {
//         _classList_add(mobileMenu, 'hidden');
//         _classList_remove(menuIconOpen, 'opacity-0');
//         _classList_add(menuIconClose, 'opacity-0');
//     }
// });

const menuIconPath = _document_querySelector('#menu-icon-path');

function closeMobileMenu() {
    _classList_remove(mobileMenu, 'visible-menu');
    _classList_add(mobileMenu, 'hidden-menu');
    _classList_remove(mobileMenuButton, 'is-active');
    setTimeout(() => {
        if (menuIconPath) _setAttribute(menuIconPath, 'd', 'M4 8h16M4 16h16');
    }, 150);
}

function openMobileMenu() {
    _classList_remove(mobileMenu, 'hidden-menu');
    _classList_add(mobileMenu, 'visible-menu');
    _classList_add(mobileMenuButton, 'is-active');
    setTimeout(() => {
        if (menuIconPath) _setAttribute(menuIconPath, 'd', 'M6 18L18 6M6 6l12 12');
    }, 150);
}

_addEventListener(mobileMenuButton, 'click', (e) => {
    e.stopPropagation();
    if (_classList(mobileMenu).contains('hidden-menu')) {
        openMobileMenu();
    } else {
        closeMobileMenu();
    }
});

mobileMenu.querySelectorAll('a').forEach(link => {
    _addEventListener(link, 'click', closeMobileMenu);
});

_addEventListener(_document, 'click', (e) => {
    if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
        if (_classList(mobileMenu).contains('visible-menu')) {
            closeMobileMenu();
        }
    }
});

_addEventListener(_w, 'resize', () => {
    if (_w.innerWidth >= 768) {
        closeMobileMenu();
    }
});
setTimeout(() => {
    closeMobileMenu();
}, 100);

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
    //     <form id="clock-form" action="/clock" emthod="get">
    //         <button id="clock-page-button" class="bg-white dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 border border-neutral-200 dark:border-neutral-700 shadow-md w-12 h-12 rounded-lg flex items-center justify-center p-2 bottom-4 right-4 fixed">
    //             <svg class="transform transition-transform duration-300 justify-center" fill="none" stroke="currentColor" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
    //                 <path
    //                 id=""
    //                 class=""
    //                 stroke-linecap="round"
    //                 stroke-linejoin="round"
    //                 stroke-width="1"
    //                 d="M6 1A1 1 0 006 11A1 1 0 006 1M4 5 6 6 9 4"
    //                 ></path>
    //             </svg>
    //         </button>
    //     </form>
    // </div>
    // `;

    
    // const clockFormHtml = '<div><form id="clock-form" action="/clock" emthod="get"><button id="clock-page-button" class="bg-white dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 border border-neutral-200 dark:border-neutral-700 shadow-md w-12 h-12 rounded-lg flex items-center justify-center p-2 bottom-4 right-4 fixed"><svg class="transform transition-transform duration-300 justify-center" fill="none" stroke="currentColor" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg"><path id="" class="" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M6 1A1 1 0 006 11A1 1 0 006 1M4 5 6 6 9 4"></path></svg></button></form></div>';
    // const clockFormHtml = '<div><form id="clock-form" action="/clock" emthod="get"><button id="clock-page-button" class="w-12 h-12 rounded-lg flex items-center justify-center p-2 bottom-4 right-4 fixed backdrop-blur-md backdrop-brightness-[0.95] dark:backdrop-brightness-[0.8] shadow shadow-lg text-neutral-500""><svg class="transform transition-transform duration-300 justify-center" fill="none" stroke="currentColor" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg"><path id="" class="" stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M6 1A1 1 0 006 11A1 1 0 006 1M4 5 6 6 9 4"></path></svg></button></form></div>';
    const clockFormHtml = '<div><form id="clock-form" action="/clock" emthod="get"><button id="clock-page-button" class="w-12 h-12 rounded-lg flex items-center justify-center p-2 bottom-4 right-4 fixed backdrop-blur-md backdrop-brightness-[0.95] dark:backdrop-brightness-[0.8] shadow shadow-lg text-neutral-500 !text-lg"><span class="material-symbols-outlined">schedule</span></button></form></div>';

    // const clockFormHtml = clockFormDiv();

    const parser = new DOMParser();
    const doc = parser.parseFromString(clockFormHtml, 'text/html');
    const clockForm = _querySelector(doc, '#clock-form');
    _appendChild(_document_body, clockForm);
}

createClockForm();

_setAttribute(_document_body, 'class', '');
// $('body').removeClass();
_classList_add(_document_body, "dark", "bg-gray-50", "dark:bg-gray-950", "min-h-screen");


[...document.querySelectorAll('a')].forEach(a=>{if(/\d+-\d+-[mf]$/.test(a.href)){a.classList.remove('btn-black','btn-blurple');a.classList.add(/\d+-1-f$/.test(a.href)?'btn-blurple':'btn-black')}});

const classShort = {
    '.btn-black': "bg-neutral-600 hover:bg-neutral-700 dark:bg-neutral-900 dark:hover:bg-neutral-700 text-white font-medium py-2 px-4 rounded-md border border-neutral-500 transition-colors duration-300 text-center",
    '.btn-blurple': "bg-gradient-to-br from-blue-600 to-indigo-600 dark:from-blue-950 dark:to-indigo-900 hover:from-blue-700 hover:to-indigo-700 dark:hover:from-blue-900 dark:hover:to-indigo-800 text-white font-medium py-2 px-4 rounded-md border border-blue-500 duration-300 shadow-md shadow-blue-600/25 hover:shadow-lg hover:shadow-blue-700/40 dark:hover:shadow-blue-900/50 active:scale-[0.98] transition-all duration-200 hover:shadow-blue-500 text-center",
};
for (const[selector, value] of Object.entries(classShort)) {
    document.querySelectorAll(selector).forEach(a=>{
        a.classList.add(...value.split(' '))
    })
};

// // Define full, uninterrupted class strings
// const Gradients = [
//   'from-slate-900 to-indigo-950',
//   'from-zinc-900 to-purple-950',
//   'from-stone-950 to-emerald-950',
//   'from-neutral-900 to-gray-950'    
// ];

// const coloredGradients = [
//   // Warm & Sunset Vibe
//   'from-amber-400 to-pink-500',
//   'from-orange-500 to-red-600',
//   'from-yellow-400 to-orange-500',
//   'from-rose-400 to-orange-300',
//   'from-amber-300 to-rose-500',
//   'from-red-500 to-pink-500',
  
//   // Cool & Aquatic
//   'from-blue-500 to-teal-400',
//   'from-cyan-400 to-blue-600',
//   'from-sky-400 to-indigo-500',
//   'from-teal-300 to-emerald-500',
//   'from-cyan-500 to-blue-500',
//   'from-sky-500 to-indigo-600',

//   // Rich Purples & Pinks
//   'from-purple-500 to-pink-500',
//   'from-indigo-500 to-purple-500',
//   'from-fuchsia-500 to-pink-500',
//   'from-violet-600 to-indigo-600',
//   'from-pink-400 to-rose-600',
//   'from-purple-400 to-fuchsia-600',

//   // Nature & Earthy Greens
//   'from-emerald-400 to-cyan-500',
//   'from-green-400 to-teal-500',
//   'from-lime-400 to-emerald-500',
//   'from-green-500 to-emerald-600',
//   'from-lime-300 to-green-500',

//   // Vibrant Multi-Color Combinations
//   'from-pink-500 via-red-500 to-yellow-500',
//   'from-fuchsia-600 via-pink-600 to-orange-500',
//   'from-cyan-400 via-teal-500 to-emerald-600',
//   'from-indigo-500 via-purple-500 to-pink-500',
//   'from-blue-400 via-indigo-500 to-purple-500',
//   'from-yellow-300 via-orange-400 to-red-500',

//   // Soft Pastels
//   'from-sky-200 to-pink-200',
//   'from-teal-200 to-lime-200',
//   'from-rose-300 to-purple-300',
//   'from-amber-200 to-pink-300',
//   'from-indigo-200 to-cyan-200'
// ];

// function getRandomDarkGradient() {
//   const randomIndex = Math.floor(Math.random() * coloredGradients.length);
//   return coloredGradients[randomIndex];
// }

// document.body.classList.add('bg-gradient-to-br', ...getRandomDarkGradient().split(' '));
})();