function submitLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // You can replace this with actual login logic.
    if (username && password) {
        alert("Logged in successfully!");
        // Redirect to another page or perform actions.
    } else {
        alert("Please enter username and password.");
    }
}




document.getElementById('backButton').addEventListener('click', function() {
    window.location.href = "popup.html";  
});


