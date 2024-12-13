document.addEventListener("DOMContentLoaded", function () {
    const createBoardButton = document.getElementById("create-board-button");
    const openBoardButton = document.getElementById("open-board-button");
    const createBoardForm = document.getElementById("create-board");
    const existingBoards = document.getElementById("existing-boards");
    const createBoardSection = document.getElementById("create-board-form");

    // Show "Create Board" form
    createBoardButton.addEventListener("click", function () {
        existingBoards.classList.add("hidden");
        createBoardSection.classList.remove("hidden");
    });

    // Show "Existing Boards"
    openBoardButton.addEventListener("click", function () {
        createBoardSection.classList.add("hidden");
        existingBoards.classList.remove("hidden");
    });

    // Handle board creation
    createBoardForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const projectName = document.getElementById("project_name").value.trim();
        const memberEmails = document.getElementById("member-emails").value.trim();

        if (!projectName) {
            showErrorMessage("Project name is required.");
            return;
        }

        fetch("/create_board", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ project_name: projectName, member_emails: memberEmails }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    alert("Board created successfully!");
                    location.reload();
                } else {
                    showErrorMessage(data.error || "An error occurred while creating the board.");
                }
            })
            .catch(() => {
                showErrorMessage("Failed to create the board. Please try again.");
            });
    });

    function showErrorMessage(message) {
        const errorElement = document.getElementById("error-message");
        errorElement.textContent = message;
        errorElement.style.display = "block";
    }
});
