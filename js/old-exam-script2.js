(async () => {
function download_file(preview = false) {
    const fileFrame = document.getElementById('pdf-viewer');
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

    // Get the title from #iframe-title (e.g., "Math 101 Midterm 2024") and add .pdf if missing
    const iframeTitle = document.getElementById('iframe-title')?.textContent || 'download';
    const filename = iframeTitle.endsWith('.pdf') ? iframeTitle : iframeTitle + '.pdf';
    
    a.download = decodeURIComponent(filename);

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

const viewerContainer = document.getElementById("pdf-viewer");
let embedPdfModulePromise = null;

async function openFile(fileData, fileName = fileData.path) {
    const source = getFileUrl(fileData.path);
    // console.log("Opening file:", fileData, "Source URL:", source);
    const sourceStr = source ? String(source) : "";

    if (!sourceStr) return;

    // Prevent reloading if the exact same file is already open
    if (viewerContainer.getAttribute("raw") === sourceStr) return;

    viewerContainer.setAttribute("raw", sourceStr);
    viewerContainer.classList.remove("hidden", "md:hidden");
    viewerContainer.style.height = 'calc(100vh - 10rem)';
    viewerContainer.style.width = '100%';

    // Clear previous viewer instance/iframe cleanly
    viewerContainer.replaceChildren();

    // Detect iOS / iPadOS (including iPadOS 13+ requesting desktop sites)
    const ua = navigator.userAgent;
    const isIOS = /iP(ad|hone|od)/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    const isSafari = /^((?!chrome|android|crios|fxios).)*safari/i.test(ua);

    if (isIOS && isSafari && false) {
        // iOS Safari has built-in native PDF rendering inside iframes (with pinch-to-zoom)
        viewerContainer.innerHTML = `
            <iframe 
                src="${sourceStr}" 
                style="width: 100%; height: 100%; border: none;" 
                title="${fileName}">
            </iframe>
        `;
    } else {
        // Desktop, Android, and iOS Chrome/Firefox:
        // Dynamically load EmbedPDF once and initialize it into #pdf-viewer
        try {
            if (!embedPdfModulePromise) {
                embedPdfModulePromise = import('https://cdn.jsdelivr.net/npm/@embedpdf/viewer@3/dist/embedpdf.js');
            }
            const { default: EmbedPDF } = await embedPdfModulePromise;
            EmbedPDF.init({
                target: '#pdf-viewer',
                src: sourceStr,
            });
        } catch (err) {
            console.error("EmbedPDF failed to initialize, falling back to iframe:", err);
            viewerContainer.innerHTML = `
                <iframe 
                    src="${sourceStr}" 
                    style="width: 100%; height: 100%; border: none;" 
                    title="${fileName}">
                </iframe>
            `;
        }
    }

    setTimeout(() => {
        if (document.visibilityState === 'visible') {
            viewerContainer?.scrollIntoView({ behavior: "smooth" });
        }
    }, 10);

    const iframeTitle = document.getElementById("iframe-title");
    console.log(fileName);
    console.log(".pdf");
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
        (terms == null || (Array.isArray(terms) ? terms.includes(+item.term) : Array.from(String(terms), Number).includes(+item.term))) &&
        (periods == null || Array.from(periods).map(p => p[0].toLowerCase()).includes(item.period[0].toLowerCase())) &&
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
        
        button.onclick = () => openFile(fileData, fileData.subjectId + ' ' + name);
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

// async function share(fileUrl, fileName = null) {
//     // const shareStatus = document.getElementById('share-status');
    
//     // shareStatus.textContent = "Initializing Sharing...";
//     try {
//         const response = await fetch(fileUrl);
//         if (!response.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//         const blob = await response.blob();

//         const file = new File([blob], fileName || fileUrl.split('/').pop(), { type: blob.type });
//         const filesArray = [file];

//         if (navigator.canShare && navigator.canShare({ files: filesArray })) {
//             // shareStatus.textContent = "Sharing...";
//             await navigator.share({
//                 files: [file],
//                 title: fileName || fileUrl.split('/').pop(),
//                 text: "Check out this file I shared!",
//             });
//             // shareStatus.textContent = "Shared!";
//         } else {
//             // shareStatus.textContent = "Sharing not supported on this device.";
//         }
//     } catch (error) {
//         console.error('Error sharing file:', error);
//         // shareStatus.textContent = "Error sharing file: " + error.message;
//     }
// }
// /**
//  * Shares a file using the native Web Share API.
//  * @param {string} fileUrl - The URL of the file to share.
//  * @param {string|null} [filename=null] - Optional custom name for the shared file.
//  * @returns {Promise<boolean>} Resolves to true if shared successfully, false otherwise.
//  */
// async function shareFile(fileUrl, filename = null) {
//   // 1. Check if the browser supports file sharing
//   if (!navigator.canShare) {
//     console.error("Web Share API is not supported in this browser.");
//     return false;
//   }

//   try {
//     // 2. Fetch the file data
//     const response = await fetch(fileUrl);
//     if (!response.ok) throw new Error("Network response was not ok");
//     const blob = await response.blob();

//     // 3. Determine the filename and extension
//     const finalFilename = filename || fileUrl.substring(fileUrl.lastIndexOf("/") + 1) || "shared-file";

//     // 4. Create a File object
//     const file = new File([blob], finalFilename, { type: blob.type });

//     // 5. Verify the browser can share this specific file type
//     if (!navigator.canShare({ files: [file] })) {
//       console.error("This browser does not support sharing this file type.");
//       return false;
//     }

//     // 6. Trigger the native share sheet
//     await navigator.share({
//       files: [file],
//       title: finalFilename,
//     });

//     return true;
//   } catch (error) {
//     console.error("Error sharing file:", error);
//     return false;
//   }
// }

async function share(fileUrl, filename = null) {
    if (!navigator.canShare) {
        console.error("Web Share API is not supported in this browser.");
        return false;
    }

    try {
        const response = await fetch(fileUrl);
        if (!response.ok) throw new Error("Network response was not ok");
        const blob = await response.blob();

        const finalFilename = filename || fileUrl.substring(fileUrl.lastIndexOf("/") + 1) || "shared-file";

        const file = new File([blob], finalFilename, { type: blob.type });

        if (!navigator.canShare({ files: [file] })) {
            console.error("This browser does not support sharing this file type.");
            return false;
        }

        await navigator.share({
            files: [file],
            title: finalFilename,
        });

        return true;
    } catch (error) {
        console.error("Error sharing file:", error);
        return false;
    }
}

const ua = navigator.userAgent;
const isIOS = /iP(ad|hone|od)/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

document.getElementById('copy-btn').addEventListener('click', () => {
    const text = document.getElementById('download-btn').href;
    navigator.clipboard.writeText(text);
    // console.log("Copied to clipboard");
});
const shareBtn = document.getElementById('share-btn');
// alert(1);
if (!isIOS) {
    // alert('ios');
    shareBtn.classList.add('hidden');
}
shareBtn.addEventListener('click', async () => {
    const text = document.getElementById('download-btn').href;
    const title = document.getElementById('iframe-title').textContent;

    await share(text, title + ".pdf");
    // console.log("Shared!");
    // alert("Shared!");
});

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