function scrapeText() {
    let text = document.body.innerText; // Get all text on the page
    return text;
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scrape") {
        let text = scrapeText();
        sendResponse({ data: text });
    }
});
