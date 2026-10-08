(async () => {
function download_file(preview = false) {
    const fileFrame = document.getElementById('file-frame');
    const rawUrl = fileFrame?.getAttribute('raw');
    const downloadButton = document.getElementById('download-btn');

    if (!rawUrl || rawUrl === window.location.href) return;

    let url = new URL(rawUrl);
    if (!preview) {
        url.pathname = url.pathname.match(/(\/[^\/]*){1}/)[0] + '/download' + url.pathname.replace(/(\/[^\/]*){2}/, '');
    }

    const href = decodeURI(url.href);
    const a = document.createElement('a');
    a.target = '_blank';
    a.href = href;

    const filename = url.pathname.split('/').pop() || 'download';
    a.download = decodeURIComponent(filename) || filename;

    document.body.appendChild(a);
    a.click();
    
    if (downloadButton) {
        downloadButton.href = href;
    }
    document.body.removeChild(a);
}
window.download_file = download_file;

function getFileUrl(path) {
    return new URL("https://api.kmu.pisc.cc/r2/file/old-exam/raw/" + path.replaceAll("\\", "/"));
}

function get_file_url(url, preview = false) {
    const parsedUrl = new URL(url);
    if (!preview) {
        parsedUrl.pathname = parsedUrl.pathname.match(/(\/[^\/]*){1}/)[0] + '/download' + parsedUrl.pathname.replace(/(\/[^\/]*){2}/, '');
    }
    return decodeURI(parsedUrl.href);
}

const frameElement = document.getElementById("file-frame");
function openFile(fileData, fileName = fileData.path) {
    const source = getFileUrl(fileData.path);
    // console.log("Opening file:", fileData, "Source URL:", source);
    const sourceStr = source ? String(source) : "";

    const finalSource = sourceStr;

    frameElement.setAttribute("sandbox", "allow-scripts allow-same-origin");
    const iframeSrc = "https://docs.google.com/viewerng/viewer?embedded=true&url=" + encodeURIComponent(finalSource);
    
    if (frameElement.src === iframeSrc) return;
    
    frameElement.src = iframeSrc;
    frameElement.setAttribute("raw", source.toString());

    if (frameElement.classList.contains("hidden")) {
        frameElement.classList.toggle("hidden");
    }
    if (frameElement.classList.contains("md:hidden")) {
        frameElement.classList.toggle("md:hidden");
    }

    frameElement.style.height = 'calc(100vh - 10rem)';
    frameElement.style.width = '100%';

    setTimeout(() => {
        if (document.visibilityState === 'visible') {
            document.getElementById("file-frame")?.scrollIntoView({ behavior: "smooth" });
        }
    }, 10);

    const iframeTitle = document.getElementById("iframe-title");
    if (iframeTitle) iframeTitle.textContent = fileName;

    const iframeContainer = document.getElementById('iframe-container');
    if (iframeContainer?.classList.contains('display-none')) {
        iframeContainer.classList.toggle("display-none");
    }

    const previewButton = document.getElementById('preview-btn');
    const downloadButton = document.getElementById('download-btn');
    if (previewButton) previewButton.href = get_file_url(source, true);
    if (downloadButton) downloadButton.href = get_file_url(source);
}

function applyXScroll(container) {
    let targetX = container.scrollLeft;
    let currentX = container.scrollLeft;
    const ease = 0.1;
    let isMoving = false;

    container.addEventListener('wheel', (e) => {
        if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;

        e.preventDefault();
        targetX += e.deltaY;

        const maxScroll = container.scrollWidth - container.clientWidth;
        targetX = Math.max(0, Math.min(targetX, maxScroll));

        if (!isMoving) {
            isMoving = true;
            requestAnimationFrame(smoothAnimation);
        }
    }, { passive: false });

    function smoothAnimation() {
        currentX += (targetX - currentX) * ease;
        container.scrollLeft = currentX;

        if (Math.abs(targetX - currentX) > 0.5) {
            requestAnimationFrame(smoothAnimation);
        } else {
            isMoving = false;
            currentX = targetX;
        }
    }

    container.addEventListener('scroll', () => {
        if (!isMoving) {
            targetX = container.scrollLeft;
            currentX = container.scrollLeft;
        }
    });
}

const table = document.getElementById("subject-table") || document.querySelector("table");
applyXScroll(table.parentElement);
table.id = "subject-table";
table.replaceChildren();

const thead = document.createElement("thead");
const headerRow = document.createElement("tr");
headerRow.classList.add("border-x", "border", "border-gray-300", "dark:border-gray-700", "text-gray-900", "dark:text-white", "bg-gray-200/60", "dark:bg-gray-800/60", "shadow-md");

const headerSubject = document.createElement("th");
headerSubject.classList.add("px-5", "py-3");
headerSubject.textContent = "Subject";
headerRow.appendChild(headerSubject);

for (let year = 2010; year <= 2025; year++) {
    const headerYear = document.createElement("th");
    headerYear.classList.add("px-5", "py-3");
    headerYear.textContent = year;
    headerRow.appendChild(headerYear);
}

thead.appendChild(headerRow);
table.appendChild(thead);

const tbody = document.createElement("tbody");
tbody.id = "table-body";
table.appendChild(tbody);

async function fetchCSVData() {
    function cleanString(str) {
        if (str.startsWith('"') && str.endsWith('"')) {
            try {
                return JSON.parse(str);
            } catch (e) {
                return str;
            }
        }
        return str;
    };

    function fileIsEP(fpath) {
        if (fpath.toLowerCase().includes("ep")) {
            return 1
        } else if (/^(?=.*ep|.*?\bS(?!1\b)\d+\b)/i.test(fpath)) {
            return 1
        } else if (/^(?!.*ep)(?!.*?\bs\d+\b).*$/i.test(fpath)) {
            return 2
        } else {
            return 0
        }   
    }

    const response = await fetch('/old-exam/files.csv');

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const csvData = await response.text();
    const commasRegex = /\s*,\s*(?=(?:[^"]*"[^"]*")*[^"]*$)/g;
    const data = csvData
        .split('\n')
        .slice(1)
        .filter(row => row.trim() !== '')
        .map(row => {
            const [fileName, year, term, period, subjectId, subjectName, fullPath, size] = row.split(commasRegex);
            const ep = fileIsEP(fullPath);
            return {
                fullPath: cleanString(fullPath),
                fileName: cleanString(fileName),
                fileSize: size,
                subjectId: subjectId,
                subjectName: cleanString(subjectName),
                year: year,
                term: term,
                period: period,
                ep: ep,
            };
        });

    return data;
}

function findFiles(data, subjects, terms=[1, 2], periods=["midterm", "final"], ep=null) {
    const filteredData = data.filter(item => 
        subjects.includes(item.subjectId) &&
        (Array.isArray(terms) ? terms.includes(+item.term) : parseInt(item.term) === terms) &&
        Array.from(periods).map(p => p[0].toLowerCase()).includes(item.period[0].toLowerCase()) &&
        (ep === null || ([+ep, 2]).includes(item.ep))
    );
    let result = {};
    for (let i = 0; i < filteredData.length; i++) {
        const item = filteredData[i];
        const year = item.year;
        result[year] = result[year] || [];
        result[year].push({
            year: item.year,
            path: item.fullPath,
            subjectId: item.subjectId,
            subjectName: item.subjectName,
            term: item.term,
            period: item.period,
            ep: item.ep,
        });
    }
    for (const [year, subjects] of Object.entries(result)) {
        if (subjects.some(item => item.ep === +ep)) {
            result[year] = subjects.filter(item => item.ep === +ep);
        }
        result[year] = result[year][0] || null;
    }
    return result;
}

function addRow(subjectFullName, subjectName, data) {
    const row = document.createElement("tr");
    row.classList.add("bg-transparent", "hover:bg-gray-100/30", "hover:dark:bg-gray-800/30", "border-x", "border", "border-gray-300", "dark:border-gray-700", "text-gray-900", "dark:text-white");

    const subjectNameCell = document.createElement("th");
    subjectNameCell.classList.add("px-5", "py-3");
    subjectNameCell.textContent = subjectFullName;
    row.appendChild(subjectNameCell);

    for (let year = 2010; year <= 2025; year++) {
        const column = document.createElement("th");
        column.classList.add("px-5", "py-3");
        row.appendChild(column);
    }
    tbody.appendChild(row);

    function addFileButton(rowElement, colIndex, fileData, name) {
        const columnElement = rowElement.children[colIndex + 1];

        const button = document.createElement("button");
        button.type = "button";
        columnElement.classList.add("hover:cursor-pointer");
        button.classList.add("text-blue-600", "dark:text-blue-400", "hover:underline", "hover:cursor-pointer");
        
        button.onclick = () => openFile(fileData, name);
        button.textContent = name;
        columnElement.appendChild(button);
    }

    function addFile(rowElement, fileName, fileData) {
        const name = fileName.split(".")[0].split(",")[0];
        const subject = name.split(" ").slice(0, -1).join(" ");
        
        const year = +fileData.year;
        const colIndex = year - 2010;

        // console.log(rowElement, colIndex, fileData, fileName);
        addFileButton(rowElement, colIndex, fileData, fileName);
    }

    for (const [year, fileData] of Object.entries(data)) {
        if (fileData) {
            // console.log(fileData);
            addFile(row, subjectName + ' ' + year, fileData);
        }
    }
}

window.Table = function() {
    return fetchCSVData().then(data => {
        function Row(subjectFullName, subjectName, ...info) {
            // console.log(subjectFullName, subjectName, info);
            if (info.length == 1) {
                addRow(subjectFullName, subjectName, info[0]);
            } else {
                addRow(subjectFullName, subjectName, findFiles(data, info.slice(3), ...info.slice(0, 3)));
            }
        }
        function Info(term, period, ep, subjects) {
            return findFiles(data, subjects, term, period, ep);
        }
        return {Row, Info};
    });
};

(async () => {
    const path = location.pathname;
    const len = path.length;
    const end3 = path.charCodeAt(len - 1) === 47 ? len - 1 : len;
    const idx2 = path.lastIndexOf('-', end3 - 1);
    const idx1 = path.lastIndexOf('-', idx2 - 1);
    const idx0 = path.lastIndexOf('/', idx1 - 1);

    const year = path.substring(idx0 + 1, idx1);
    const term = path.substring(idx1 + 1, idx2);
    const period = path.substring(idx2 + 1, end3);

    const text = [
        `Old Exam Year ${year} Term ${term} ${period === "f" ? "Final" : "Midterm"}`,
        `ข้อสอบเก่าปี ${year} เทอม ${term} ${period === "f" ? "ปลายภาค" : "กลางภาค"}`,
    ];

    const pageTitle = document.querySelector("h1");
    if (pageTitle) {
        pageTitle.innerHTML = `<l-en>${text[0]}</l-en><l-th>${text[1]}</l-th>`;
    }

    const title = document.querySelector("title");
    function updatePageTitle() {
        const langMode = localStorage.lang || "en";
        if (title) {
            title.textContent = text[langMode === "en" ? 0 : 1];
        }
    }

    updatePageTitle();
    window.addEventListener('storage', () => {
        updatePageTitle();
    });
})();
})();