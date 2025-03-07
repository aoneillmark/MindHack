chrome.action.onClicked.addListener(() => {
    chrome.windows.create({
      url: "popup.html",
      type: "popup",
      width: 800,
      height: 400
    });
  });

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


document.addEventListener('DOMContentLoaded', function() {
    const profilePic = document.querySelector('.profile-pic');
    profilePic.addEventListener('click', goToLogin);
});

function goToLogin() {
    window.location.href = "login.html";  // Redirect to login.html page
}