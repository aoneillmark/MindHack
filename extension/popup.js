document.getElementById("scrapeBtn").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            function: scrapeAndDownload
        });
    });
});

function scrapeAndDownload() {
    let text = document.body.innerText;
    let blob = new Blob([text], { type: "text/plain" });
    let url = URL.createObjectURL(blob);

    let a = document.createElement("a");
    a.href = url;
    a.download = "scraped_text.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
