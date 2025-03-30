document
  .querySelector("form")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevents page reload

    const formData = new FormData(this); // Capture form data correctly inside event listener

    try {
      const response = await fetch("/api/auth/signup", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      const data = await response.json();
      console.log("Success:", data);

      window.location.href = "login.html"; // Redirect after successful signup
    } catch (error) {
      console.error("Error:", error);
    }
  });
