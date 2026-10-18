const toggleButton = document.getElementById('toggleButton');
let isEnabled = true;

chrome.storage.local.get(['isEnabled'], (result) => {
    if (result.isEnabled !== undefined) {
        isEnabled = result.isEnabled;
    }
    updateButtonText();
});

function updateButtonText() {
    if (isEnabled) {
        toggleButton.textContent = 'ON';
        toggleButton.style.backgroundColor = '#4CAF50';
    } else {
        toggleButton.textContent = 'OFF';
        toggleButton.style.backgroundColor = '#f44336';
    }
}

toggleButton.addEventListener('click', () => {
    isEnabled = !isEnabled;
    const status = isEnabled ? 'ON' : 'OFF';

    chrome.storage.local.set({ isEnabled: isEnabled }, () => {
        updateButtonText();
        
        fetch('http://127.0.0.1:5002/status_update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: status })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Server state updated:", data.new_status);
        })
        .catch(error => {
            console.error('Error updating server status:', error);
        });

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs && tabs.length > 0) {
                 chrome.tabs.sendMessage(tabs[0].id, {status: status});
            }
        });
    });
});