document.addEventListener("DOMContentLoaded", function () {
    console.log("script.js loaded successfully!");

    const scheduleForm = document.getElementById("scheduleForm");
    const submitButton = scheduleForm.querySelector("button[type='submit']");
    const responseMessage = document.getElementById("responseMessage");
    let loading = false;

    if (scheduleForm) {
        scheduleForm.addEventListener("submit", function (event) {
            event.preventDefault();

            // Show loading message if a request is already being processed
            if (loading) {
                responseMessage.innerText = "A request is already being processed. Your submission has been queued.";
                return;
            }

            // Mark as loading to handle feedback only (without disabling the button)
            loading = true;
            responseMessage.innerText = "Processing your request...";  // User feedback
            submitButton.classList.add("loading");

            // Collect form data
            const accountDescription = document.getElementById("accountDescription").value;
            const numPosts = document.getElementById("numPosts").value;
            const timeInterval = document.getElementById("timeInterval").value;
            const postIdeas = document.getElementById("postIdeas").value.split("\n").filter(idea => idea.trim() !== "") ;

            // Send POST request to the backend
            fetch("/schedule_post", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    account_description: accountDescription,
                    num_posts: numPosts,
                    time_interval: timeInterval,
                    post_ideas: postIdeas
                })
            })
                .then(response => {
                    loading = false;  // Reset loading state when response is received
                    submitButton.classList.remove("loading");

                    if (!response.ok) {
                        throw new Error("A request is already being processed.");
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Response from server:", data);
                    responseMessage.innerText = data.message;  // Show success message
                })
                .catch(error => {
                    console.error("Error:", error);
                    responseMessage.innerText = error.message;  // Show error message
                });
        });
    }
});
