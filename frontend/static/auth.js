console.log("it is printing");
async function checkAndFetch(apiEndpoint) {
  const response = await fetch(apiEndpoint, {
    method: "GET",
    credentials: "include", // Include cookies for authentication
  });

  console.log("fgkrlngclrt", response.status);
  if (response.status !== 200) {
    console.log("Unauthorized or error response, redirecting to login...");
    window.location.href = "/login.html"; // Redirect to login page
    return false;
  }

  return await response.json(); // Return the response if successful
}
