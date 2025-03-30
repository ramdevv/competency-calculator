const container = document.getElementById("questions_id");
const start = document.getElementById("fetchScores");
start.addEventListener("click", async () => {
  console.log(" the button was pressed ");
  try {
    const response = await fetch("/api/scores/evaluation", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json(); // Parse JSON response
    container.innerHTML = ""; // Clear previous content
    container.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    console.error("Error fetching scores:", error);
  }
});
