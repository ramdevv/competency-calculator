const dashbutton = document.getElementById("dashid");
const button = document.getElementById("buttonid");
const logout = document.getElementById("logout");
button.addEventListener("click", async () => {
  console.log("the button was pressed ");
  window.location.href = "aptitude.html";
});

dashbutton.addEventListener("click", async () => {
  console.log("the button was pressed ");
  window.location.href = "dashboard.html";
});
logout.addEventListener("click", async () => {
  console.log("Logout button pressed");

  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      credentials: "include",
    });
    if (response.ok) {
      console.log("Session cleared, redirecting...");
      window.location.href = "sign_in.html";
    } else {
      console.error("Logout failed");
    }
  } catch (error) {
    console.error("Error during logout:", error);
  }
});
