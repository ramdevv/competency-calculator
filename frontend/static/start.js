// Get buttons
const signinButton = document.getElementById("signupButton");
const loginButton = document.getElementById("loginButton");

// Add event listeners (correct spelling)
signinButton.addEventListener("click", (event) => {
  // Fixed spelling
  event.preventDefault(); // Prevent form submission
  console.log("Signup button was pressed");
  window.location.href = "sign_in.html";
});

loginButton.addEventListener("click", (event) => {
  // Fixed spelling
  event.preventDefault(); // Prevent form submission
  console.log("Login button was pressed");
  window.location.href = "login.html";
});
