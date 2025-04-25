// scripts.js

// Runs when the page is loaded
document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded successfully!");

    // Optional: Alert on homepage
    const greeting = document.querySelector(".navbar h2");
    if (greeting) {
        greeting.addEventListener("click", () => {
            alert("Welcome to your dashboard!");
        });
    }

    // Optional: Confirm before logout
    const logoutLink = document.querySelector(".nav-links a[href*='logout']");
    if (logoutLink) {
        logoutLink.addEventListener("click", function (e) {
            const confirmLogout = confirm("Are you sure you want to log out?");
            if (!confirmLogout) e.preventDefault();
        });
    }
});
