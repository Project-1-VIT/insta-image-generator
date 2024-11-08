document.addEventListener("DOMContentLoaded", function() {
    console.log("script.js loaded successfully!");

    const scheduleForm = document.getElementById("scheduleForm");
    const submitButton = scheduleForm.querySelector("button[type='submit']");
    let loading = false;

    if (scheduleForm) {
        scheduleForm.addEventListener("submit", function(event) {
            event.preventDefault();

            if (loading) return;  // Prevent further submissions if already loading
            loading = true;
            submitButton.disabled = true;

            const accountDescription = document.getElementById("accountDescription").value;
            const numPosts = document.getElementById("numPosts").value;
            const timeInterval = document.getElementById("timeInterval").value;
            const postIdeas = document.getElementById("postIdeas").value;

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
                loading = false;
                submitButton.disabled = false; // Re-enable on response
                if (!response.ok) {
                    throw new Error("Request is already being processed.");
                }
                return response.json();
            })
            .then(data => {
                console.log("Response from server:", data);
                document.getElementById("responseMessage").innerText = data.message;
            })
            .catch(error => {
                console.error("Error:", error);
                document.getElementById("responseMessage").innerText = error.message;
            });
        });
    }
});
