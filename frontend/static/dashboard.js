document.addEventListener("DOMContentLoaded", async function () {
  const response = await fetch("/api/dashboard", {
    method: "GET",
    credentials: "include", // Ensures cookies are sent
  });

  if (response.ok) {
    const data = await response.json();
    console.log(data);
  } else {
    console.log("Failed to print the quiz");
  }
});
