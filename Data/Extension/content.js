console.log("Content script loaded.");

// to on/off the server, default is on
let serverEnabled = true;

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.status === 'ON') {
        serverEnabled = true;
    } else if (msg.status === 'OFF') {
        serverEnabled = false;
        if (subtitleDiv) subtitleDiv.innerText = '';
        if (originalDiv) originalDiv.innerHTML = '';
        hideTooltip();
    }
});

let subtitleDiv, originalDiv, tooltipDiv;

try {
    subtitleDiv = document.createElement("div");
    subtitleDiv.id = "subtitle-overlay";
    subtitleDiv.innerText = "Loading subtitles...";
    subtitleDiv.style.position = "fixed";
    subtitleDiv.style.bottom = "0px";
    subtitleDiv.style.left = "50%";
    subtitleDiv.style.transform = "translateX(-50%)";
    subtitleDiv.style.zIndex = "999999";
    subtitleDiv.style.background = "transparent";
    subtitleDiv.style.color = "#fff";
    subtitleDiv.style.padding = "5px 10px";
    subtitleDiv.style.borderRadius = "5px";
    subtitleDiv.style.maxWidth = "80%";
    subtitleDiv.style.fontSize = "32px";
    document.body.appendChild(subtitleDiv);

    originalDiv = document.createElement("div");
    originalDiv.id = "original-overlay";
    originalDiv.style.position = "fixed";
    originalDiv.style.bottom = "50px";
    originalDiv.style.left = "50%";
    originalDiv.style.transform = "translateX(-50%)";
    originalDiv.style.zIndex = "999998";
    document.body.appendChild(originalDiv);

    tooltipDiv = document.createElement("div");
    tooltipDiv.id = "word-tooltip";
    tooltipDiv.style.position = "fixed";
    tooltipDiv.style.zIndex = "999999";
    tooltipDiv.style.background = "rgba(0,0,0,0.8)";
    tooltipDiv.style.color = "#fff";
    tooltipDiv.style.padding = "3px 6px";
    tooltipDiv.style.borderRadius = "4px";
    tooltipDiv.style.fontSize = "20px";
    tooltipDiv.style.display = "none";
    document.body.appendChild(tooltipDiv);
} catch (err) {
    console.warn("Extension doesn't work on this site.", err);
}

let lastHoveredWord = null;

function displayTooltip(text, x = 20, y = 20) {
    if (!tooltipDiv)
        return;
    tooltipDiv.innerText = text;
    tooltipDiv.style.left = x + "px";
    tooltipDiv.style.top = y + "px";
    tooltipDiv.style.display = "block";
}

function hideTooltip() {
    if (!tooltipDiv)
        return;
    tooltipDiv.style.display = "none";
}

function fetchDefinition(word) {
    displayTooltip("Loading definition...");
    chrome.runtime.sendMessage({ action: "getDefinition", word }, (data) => {
        displayTooltip(data.definition || `No definition for "${word}"`);
    });
}

function updateSubtitle() {
    chrome.runtime.sendMessage({ action: "getOCR" }, (data) => {
        if (!data)
            return;

        if (!serverEnabled)
            return;

        subtitleDiv.innerText = data.text || "";
        originalDiv.innerHTML = "";

        const lines = data.original_lines_data || [];
        const borderBoxes = data.border_box || [];

        const scaleX = 1;
        const scaleY = 1;

        const ct = 180;
        const offsetX = data.screenshot_left || 0;
        const offsetY = data.screenshot_top || 0;

        // hitbox for each line
        lines.forEach((lineData, index) => {
            const box = borderBoxes[index];
            if (!box)
                return;

            const [topLeft, bottomRight, width, height] = box;

            const lineHitbox = document.createElement('div');

            lineHitbox.className = 'line-hitbox';
            lineHitbox.style.position = 'absolute';

            // Position and size using the information from the screenshot
            lineHitbox.style.left = `${offsetX + topLeft[0] * scaleX}px`;
            lineHitbox.style.top = `${offsetY + topLeft[1] * scaleY - ct}px`;
            lineHitbox.style.width = `${width * scaleX}px`;
            lineHitbox.style.height = `${height * scaleY}px`;


            lineHitbox.style.background = 'rgba(0,0,0,0)';
            lineHitbox.style.pointerEvents = 'auto';
            lineHitbox.style.cursor = 'default';
            lineHitbox.style.zIndex = '999998';

            lineHitbox.onmousemove = (e) => {
                const rect = e.currentTarget.getBoundingClientRect();
                const mouseX = e.clientX - rect.left;
                const mousePercent = (mouseX / rect.width) * 100;

                for (const interval of lineData.word_intervals || []) {
                    if (mousePercent >= interval.procent_start && mousePercent <= interval.procent_end) {
                        if (interval.word !== lastHoveredWord) {
                            fetchDefinition(interval.word);
                            lastHoveredWord = interval.word;
                        }
                        return;
                    }
                }
                hideTooltip();
                lastHoveredWord = null;
            };

            lineHitbox.onmouseleave = () => {
                hideTooltip();
                lastHoveredWord = null;
            };

            originalDiv.appendChild(lineHitbox);
        });
    });
}

setInterval(updateSubtitle, 700);
