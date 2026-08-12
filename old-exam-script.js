(()=>{

const _document = document;
const _document_getElementById = id => _document.getElementById(id);
const _document_createElement = tag => _document.createElement(tag);
const _appendChild = (element, child) => element.appendChild(child);
const _classList = element => element.classList;
const _classList_add = (element, ...className) => _classList(element).add(...className);
const _classList_remove = (element, ...className) => _classList(element).remove(...className);
const _classList_toggle = (element, ...className) => _classList(element).toggle(...className);
const _classList_contains = (element, className) => _classList(element).contains(className);
const _addEventListener = (element, event, callback) => element.addEventListener(event, callback);
const _querySelector = (element, selector) => element.querySelector(selector);
const _querySelectorAll = (element, selector) => element.querySelectorAll(selector);
const _innerHTML = (element, html) => element.innerHTML = html;
const _setAttribute = (element, attribute, value) => element.setAttribute(attribute, value);

// window.addEventListener('scroll', function(event) {
//     const navHeight = document.querySelector('nav').offsetHeight;
//     const iframe = _document_getElementById('file-frame');
//     const iframeContainer = _document_getElementById('iframe-container');
//     const rect = iframe.getBoundingClientRect();
//     if (rect.top <= window.innerHeight - navHeight && rect.bottom >= 0) {
//         iframe.style.height = `calc(100vh - ${navHeight}px)`;
//         iframe.style.width = '100%';
//         iframe.classList.remove('hidden');
//     } else {
//         iframe.style.height = '';
//         iframe.style.width = '';
//         iframe.classList.add('hidden');
//     }
// });

function get_file_url(url, preview = false) {
    url = new URL(url);
    if (preview) {
        url.pathname = '/file'+url.pathname.replace(/(\/[^\/]*){1}/,'')
    }
    
    return decodeURI(url.href);
}

function download_file(preview = false) {

    const fileFrame = _document_getElementById('file-frame');
    const rawUrl = fileFrame.getAttribute('raw');
    const downloadButton = _document_getElementById('download-btn');
    
    // Safety check in case the attribute is missing
    if (!rawUrl) return; 

    // Safety fallback check if the iframe hasn't loaded a URL yet
    if (!rawUrl || rawUrl === window.location.href) return;

    let url = new URL(rawUrl);
    // url.host = "dl.kmu.pisc.cc";
    if (preview) {
        // url = url.origin+['/file',...url.pathname.split('/').slice(2)].join('/')
        url.pathname = '/file'+url.pathname.replace(/(\/[^\/]*){1}/,'')
    }
    
    const a = _document_createElement('a');
    a.href = decodeURI(url.href);
    
    // Extract the actual filename from the end of the pathname
    const filename = url.pathname.split('/').pop() || 'download';
    a.download = decodeURIComponent(filename) || filename;
    
    _appendChild(document.body, a);
    a.click();
    // downloadButton.href = a.href;
    downloadButton.href = decodeURI(url.href);
    document.body.removeChild(a);
};
window.download_file = download_file;

function isIOS() {
    const userAgent = navigator.userAgent;
    const platform = navigator.platform;

    // Check for common iOS user agent strings
    if (/iPad|iPhone|iPod/.test(userAgent)) {
        return true;
    }

    // Specific check for iPad on iOS 13+ which might report as 'MacIntel' platform
    if (platform === 'MacIntel' && navigator.maxTouchPoints > 1) {
        return true;
    }

    return false;
};

function getFileUrl(path) {
    const [, , seg2, seg3] = new URL(window.location.href).pathname.split('/');
    var Url = new URL(`https://api.kmu.pisc.cc/download/old-exam/${seg2}/${seg3}/${path}`);
    return Url;
};

function openFile(path) {
    var source = getFileUrl(path);
    const FrameElement = _document_getElementById("file-frame");
    const sourceStr = source ? String(source) : "";
    const cacheBuster = sourceStr.includes('?') ? `&cb=${Date.now()}` : `?cb=${Date.now()}`;
    const finalSource = sourceStr + cacheBuster;
    FrameElement.setAttribute("sandbox", "allow-scripts allow-same-origin");
    const iframeSrc = "https://docs.google.com/viewerng/viewer?embedded=true&url=" + encodeURIComponent(finalSource);
    if (frameElement?.src === iframeSrc) return;
    FrameElement.src = iframeSrc;
    // FrameElement.src = "https://docs.google.com/viewerng/viewer?embedded=true&url=" + encodeURIComponent(source);
    FrameElement.setAttribute("raw", source);
    if (_classList_contains(FrameElement, "hidden")){
        _classList_toggle(FrameElement, "hidden");
    }
    if (_classList_contains(FrameElement, "md:hidden")){
        _classList_toggle(FrameElement, "md:hidden");
    }
    // var navHeight = document.querySelector('nav').offsetHeight;
    // FrameElement.style.height = `calc(100vh - ${navHeight}px)`;
    FrameElement.style.height = `calc(100vh - 10rem)`;
    FrameElement.style.width = '100%';
    // window.location.href = "#file-frame";
    // FrameElement.addEventListener("load", () => {
    //     // window.scrollTo(0,document.body.scrollHeight);
    // })
    // FrameElement.addEventListener('visibilitychange', () => {
    setTimeout(() => {
        if (document.visibilityState === 'visible') {
            _document_getElementById("file-frame")?.scrollIntoView({ behavior: "smooth" })
        }
    }, 10);

    const IFrameTitle = _document_getElementById("iframe-title");
    IFrameTitle.textContent = path;

    const iframeContainer = _document_getElementById('iframe-container');
    if (_classList_contains(iframeContainer, 'display-none')) {
        // iframeContainer.classList.remove('display-none');
        _classList_toggle(iframeContainer, "display-none");
    }

    const previewButton = _document_getElementById('preview-btn');
    const downloadButton = _document_getElementById('download-btn');
    previewButton.href = get_file_url(source, true);
    downloadButton.href = get_file_url(source);
};

// function applyXScroll(t){let e=t.scrollLeft,l=t.scrollLeft,a=!1;function n(){l+=.1*(e-l),t.scrollLeft=l,Math.abs(e-l)>.5?requestAnimationFrame(n):(a=!1,l=e)}t.addEventListener("wheel",l=>{if(Math.abs(l.deltaX)>Math.abs(l.deltaY))return;l.preventDefault(),e+=1*l.deltaY;const r=t.scrollWidth-t.clientWidth;e=Math.max(0,Math.min(e,r)),a||(a=!0,requestAnimationFrame(n))},{passive:!1}),t.addEventListener("scroll",()=>{a||(e=t.scrollLeft,l=t.scrollLeft)})};
function applyXScroll(container) {
    let targetX = container.scrollLeft;
    let currentX = container.scrollLeft;
    const ease = 0.1; // Smoothness factor (Lower = smoother/slower, Higher = snappier)
    let isMoving = false;
    
    // 1. Capture the mouse wheel input
    container.addEventListener('wheel', (e) => {
        // Check if the user is using a trackpad (horizontal delta exists)
        // If they are on a trackpad, let the browser handle it natively
        if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
            return; 
        }
        
        e.preventDefault();
        
        // Calculate where the scroll should ideally land
        // Multiply e.deltaY to increase or decrease scroll distance per tick
        targetX += e.deltaY * 1; 
        
        // Keep target boundaries clamped within the container limits
        const maxScroll = container.scrollWidth - container.clientWidth;
        targetX = Math.max(0, Math.min(targetX, maxScroll));
        
        // Start the animation loop if it isn't running
        if (!isMoving) {
            isMoving = true;
            requestAnimationFrame(smoothAnimation);
        }
    }, { passive: false });
    
    // 2. The Animation Loop (Lerp engine)
    function smoothAnimation() {
        // Linear Interpolation calculation
        currentX += (targetX - currentX) * ease;
        
        container.scrollLeft = currentX;
        
        // Keep animating until the difference is negligible
        if (Math.abs(targetX - currentX) > 0.5) {
            requestAnimationFrame(smoothAnimation);
        } else {
            isMoving = false;
            currentX = targetX; // Snap exactly to target at the end
        }
    }
    
    // 3. Keep the target synced if the user drags the native scrollbar/swipes
    _addEventListener(container, 'scroll', () => {
        if (!isMoving) {
            targetX = container.scrollLeft;
            currentX = container.scrollLeft;
        }
    });
};

const table = _document_getElementById("subject-table") || document.querySelector("table");
applyXScroll(table.parentElement);
table.id = "subject-table";
table.replaceChildren();

const thead = _document_createElement("thead");

const headerRow = _document_createElement("tr");
_classList_add(headerRow, "border-x", "border", "border-gray-300", "dark:border-gray-700", "text-gray-900", "dark:text-white", "bg-gray-200/60", "dark:bg-gray-800/60", "shadow-md");

const headerSubject = _document_createElement("th");
_classList_add(headerSubject, "px-5", "py-3");
headerSubject.textContent = "Subject";
_appendChild(headerRow, headerSubject);

for (let i = 2010; i <= 2025; i++) {
    const headerYear = _document_createElement("th");
    // headerYear.classList.add("px-5", "py-3");
    _classList_add(headerYear, "px-5", "py-3");
    headerYear.textContent = i;
    _appendChild(headerRow, headerYear);
};

_appendChild(thead, headerRow);
_appendChild(table, thead);

// const tbody = _document_getElementById("table-body");
const tbody = _document_createElement("tbody");
tbody.id = "table-body";
_appendChild(table, tbody);

for (let i = 0; i < SubjectsFull.length; i++) {
    const row = _document_createElement("tr");
    // row.classList.add("bg-white", "dark:bg-gray-800", "hover:bg-gray-100", "dark:hover:bg-gray-700", "border-x", "border", "border-gray-300", "dark:border-gray-700", "text-gray-900", "dark:text-white");
    _classList_add(row, "bg-transparent", "hover:bg-gray-100/30", "hover:dark:bg-gray-800/30", "border-x", "border", "border-gray-300", "dark:border-gray-700", "text-gray-900", "dark:text-white");
    const subjectName = _document_createElement("th");
    _classList_add(subjectName, "px-5", "py-3");
    subjectName.textContent = SubjectsFull[i];
    _appendChild(row, subjectName);
    for (let j = 2010; j <= 2025; j++) {
        const column = _document_createElement("th");
        _classList_add(column, "px-5", "py-3");
        _appendChild(row, column);
    };
    _appendChild(tbody, row);
};

function addFileButton(row, column, file, name) {
    // console.log(row, column, file, name);
    var tbody = _document_getElementById("table-body");
    var rowElement = tbody.children[row];
    var columnElement = rowElement.children[column + 1];
    var button = _document_createElement("button");
    button.type = "button";
    _classList_add(columnElement, "hover:cursor-pointer")
    _classList_add(button, "text-blue-600", "dark:text-blue-400", "hover:underline", "hover:cursor-pointer");
    // button.href = file;
    button.onclick = function() {
        openFile(file);
    };
    button.textContent = name;
    _appendChild(columnElement, button);
};
function addFile(file) {
    var name = file.split(".")[0].split(",")[0];
    var subject = name.split(" ").slice(0, -1).join(" ");
    if (!Subjects.includes(subject)) {return;};
    var row = parseInt(Subjects.indexOf(subject), 10);
    var year = parseInt(name.split(" ").at(-1), 10);
    var column = year - 2010;
    // if (year != 2024) {
    addFileButton(row, column, file, name);
    // }
};
// fetch(`${window.location.protocol}//con.${window.location.host}${window.location.pathname}`).then(a => a.json()).then(files => {
fetch(`${window.location.protocol}//api.kmu.pisc.cc/list${window.location.pathname}`).then(a => a.json()).then(files => {
    files.items.forEach(file => {
        if (file.name != "index.html" && file.type == "File") {
            addFile(file.name);
        };
    });
});

})();