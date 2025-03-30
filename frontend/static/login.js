const authForm = document.getElementById("authForm"); // Get the form element
const errorMessage = document.getElementById("errorMessage");

authForm.addEventListener("submit", async (event) => {
  event.preventDefault(); // Prevent default form submission

  // Get form data
  const formData = new FormData(authForm);
  const username = formData.get("username").trim();
  const password = formData.get("password").trim();

  if (!username || !password) {
    errorMessage.textContent = "Username and password are required.";
    return;
  }

  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, password: password }),
    });

    const data = await response.json();
    console.log("fbghjukiuo", response.ok);
    if (response.ok) {
      console.log("Login successful");
      window.location.href = "home.html";
    } else {
      errorMessage.textContent = data.error || "Login failed. Try again.";
    }
  } catch (error) {
    console.error("Network error:", error);
    errorMessage.textContent = "Network error. Please try again later.";
  }
});
