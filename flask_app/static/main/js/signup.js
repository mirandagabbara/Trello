document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");
    const errorMessage = document.getElementById("error-message");

    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            event.preventDefault(); 

            const email = document.getElementById("signup-email").value.trim();
            const password = document.getElementById("signup-password").value.trim();

            if (!email || !password) {
                showErrorMessage("Email and password are required.");
                return;
            }

            // Send data to server
            fetch("/processsignup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ email, password }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        window.location.href = "/login"; // Redirect to login page
                    } else {
                        showErrorMessage(data.error || "Signup failed.");
                    }
                })
                .catch(() => {
                    showErrorMessage("An error occurred. Please try again.");
                });
        });
    }

    function showErrorMessage(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = "block"; // Ensure the error message is visible
    }
});
