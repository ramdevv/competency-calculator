document.addEventListener("DOMContentLoaded", function () {
  const tableContainer = document.getElementById("score_table");
  const scoreCard = document.getElementById("score_card");
  const loadingElement = document.getElementById("loading");
  const fetchButton = document.getElementById("fetchScores");

  // Always fetch scores when the page loads - no need to click button
  fetchScores();

  // Also allow fetching via button click
  fetchButton.addEventListener("click", fetchScores);

  async function fetchScores() {
    // Show loading state
    loadingElement.style.display = "flex";
    fetchButton.disabled = true;

    try {
      console.log("Fetching scores from API...");
      const response = await fetch("/api/scores/evaluation", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      // Get the data as text first for debugging
      const responseText = await response.text();
      console.log("Raw API response:", responseText);

      // Parse the text to JSON
      let data;
      try {
        data = JSON.parse(responseText);
        console.log("Parsed data:", data);
      } catch (parseError) {
        console.error("Failed to parse JSON:", parseError);
        throw new Error("Invalid JSON response from server");
      }

      // Hide loading state
      loadingElement.style.display = "none";

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      if (data.message) {
        console.log("Message received instead of scores:", data.message);
        tableContainer.innerHTML = `<div class="error-message">${data.message}</div>`;
        scoreCard.style.display = "block";
        return;
      }

      // Directly create the table HTML - more reliable than DOM methods
      let tableHTML = '<table class="score-table">';

      // Flexible approach - try to detect the structure of the data
      if (typeof data === "object" && !Array.isArray(data)) {
        // Case 1: Expected properties
        if (
          data.hasOwnProperty("apti_score") ||
          data.hasOwnProperty("comni_score") ||
          data.hasOwnProperty("technical_score") ||
          data.hasOwnProperty("total_competency")
        ) {
          tableHTML += `
            <tr>
              <th>Aptitude</th>
              <th>Communication</th>
              <th>Technical</th>
              <th>Total Competency</th>
            </tr>
            <tr>
              <td class="score-cell">${formatScore(
                data.apti_score || "N/A"
              )}</td>
              <td class="score-cell">${formatScore(
                data.comni_score || "N/A"
              )}</td>
              <td class="score-cell">${formatScore(
                data.technical_score || "N/A"
              )}</td>
              <td class="score-cell total-score">${formatScore(
                data.total_competency || "N/A"
              )}</td>
            </tr>
          `;
        }
        // Case 2: Generic object with different properties
        else {
          const keys = Object.keys(data);

          // Header row
          tableHTML += "<tr>";
          keys.forEach((key) => {
            tableHTML += `<th>${formatHeader(key)}</th>`;
          });
          tableHTML += "</tr>";

          // Data row
          tableHTML += "<tr>";
          keys.forEach((key, index) => {
            const cellClass =
              index === keys.length - 1
                ? "score-cell total-score"
                : "score-cell";
            tableHTML += `<td class="${cellClass}">${formatScore(
              data[key]
            )}</td>`;
          });
          tableHTML += "</tr>";
        }
      }
      // Case 3: Array of objects
      else if (Array.isArray(data) && data.length > 0) {
        const firstItem = data[0];
        const keys = Object.keys(firstItem);

        // Header row
        tableHTML += "<tr>";
        keys.forEach((key) => {
          tableHTML += `<th>${formatHeader(key)}</th>`;
        });
        tableHTML += "</tr>";

        // Data rows for each item
        data.forEach((item) => {
          tableHTML += "<tr>";
          keys.forEach((key) => {
            tableHTML += `<td class="score-cell">${formatScore(
              item[key]
            )}</td>`;
          });
          tableHTML += "</tr>";
        });
      }
      // Case 4: Fallback for unexpected data
      else {
        tableHTML += `
          <tr>
            <th>Data</th>
          </tr>
          <tr>
            <td>${JSON.stringify(data)}</td>
          </tr>
        `;
      }

      tableHTML += "</table>";

      // Insert the table
      tableContainer.innerHTML = tableHTML;
      scoreCard.style.display = "block";
      fetchButton.style.display = "none";
    } catch (error) {
      console.error("Error details:", error);
      loadingElement.style.display = "none";
      tableContainer.innerHTML = `<div class="error-message">Failed to load your evaluation results. Please try again later.<br><small>${error.message}</small></div>`;
      scoreCard.style.display = "block";
      fetchButton.disabled = false;
    }
  }

  // Helper function to format score values
  function formatScore(score) {
    if (score === undefined || score === null) return "N/A";
    return typeof score === "number" ? score.toFixed(1) : score;
  }

  // Helper function to format header text
  function formatHeader(text) {
    return text
      .replace(/_/g, " ")
      .split(" ")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  }
});
