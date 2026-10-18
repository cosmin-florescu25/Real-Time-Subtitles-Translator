chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "getOCR") {
        fetch("http://127.0.0.1:5002/ocr")
            .then(res => res.json())
            .then(data => sendResponse(data))
            .catch(err => sendResponse({ text: "", error: err.message }));
        return true;
    }

    if (msg.action === "getDefinition") {
        const word = msg.word;
        fetch(`http://127.0.0.1:5002/definition?word=${encodeURIComponent(word)}`)
            .then(res => res.json())
            .then(data => sendResponse(data))
            .catch(err => sendResponse({ definition: `Error: ${err.message}` }));
        return true;
    }
});
