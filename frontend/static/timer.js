document.addEventListener("DOMContentLoaded", function () {
  let timer;
  let timeLeft = 300; // 5 minutes in seconds
  const startButton = document.getElementById("button_id");
  const submitButton = document.getElementById("submit_id");

  // Create timer element now but keep it hidden
  const timerElement = document.createElement("div");
  timerElement.id = "quiz-timer";
  timerElement.className = "timer-container";
  timerElement.style.display = "none"; // Hide initially

  // Style the timer inline to ensure it works
  timerElement.style.backgroundColor = "#2d2d2d";
  timerElement.style.color = "#ffffff";
  timerElement.style.padding = "15px";
  timerElement.style.borderRadius = "6px";
  timerElement.style.marginBottom = "20px";
  timerElement.style.textAlign = "center";
  timerElement.style.fontSize = "18px";
  timerElement.style.fontWeight = "300";
  timerElement.style.letterSpacing = "1px";
  timerElement.style.borderLeft = "4px solid #666";

  // Add timer content
  timerElement.innerHTML = `
  <span>Time Remaining:</span>
  <span id="time-display">5:00</span>
`;

  // Add timer to the quiz container immediately
  const quizContainer = document.querySelector(".quiz-container");
  quizContainer.insertBefore(
    timerElement,
    document.getElementById("ques_content_id")
  );

  function startTimer() {
    // Show the timer
    timerElement.style.display = "flex";
    timerElement.style.justifyContent = "space-between";
    timerElement.style.alignItems = "center";

    // Reset the time if needed
    timeLeft = 300;
    updateTimerDisplay();

    // Start the countdown
    clearInterval(timer); // Clear any existing timer
    timer = setInterval(updateTimer, 1000);
  }

  function updateTimerDisplay() {
    // Format the time
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    const formattedTime = `${minutes}:${
      seconds < 10 ? "0" + seconds : seconds
    }`;

    // Update the display
    const timeDisplay = document.getElementById("time-display");
    if (timeDisplay) {
      timeDisplay.textContent = formattedTime;
    }
  }

  function updateTimer() {
    timeLeft--;
    updateTimerDisplay();

    // Visual indicator when time is running low (less than 1 minute)
    if (timeLeft < 60) {
      const timeDisplay = document.getElementById("time-display");
      if (timeDisplay) {
        timeDisplay.style.color = "#ff6b6b";
        document.getElementById("quiz-timer").style.borderLeft =
          "4px solid #ff6b6b";

        // Add pulse animation when time is very low (less than 30 seconds)
        if (timeLeft < 30) {
          timeDisplay.style.animation = "pulse 1s infinite";
          // Add the CSS animation if not already added
          if (!document.getElementById("timer-animation-style")) {
            const style = document.createElement("style");
            style.id = "timer-animation-style";
            style.innerHTML = `
            @keyframes pulse {
              0% { opacity: 1; }
              50% { opacity: 0.5; }
              100% { opacity: 1; }
            }
          `;
            document.head.appendChild(style);
          }
        }
      }
    }

    // Auto-submit when timer reaches zero
    if (timeLeft <= 0) {
      clearInterval(timer);
      autoSubmitQuiz();
    }
  }

  function autoSubmitQuiz() {
    // Find and trigger the submit button
    if (submitButton) {
      submitButton.click();
    } else {
      // Fallback in case the button isn't found
      alert("Time's up! Your quiz has been automatically submitted.");
      // You may need to implement custom submission logic here
    }
  }

  // Attach event listeners
  if (startButton) {
    startButton.addEventListener("click", function () {
      startTimer();

      // Show the submit button if it's hidden
      if (submitButton) {
        submitButton.classList.remove("hidden");
      }
    });
  }

  if (submitButton) {
    submitButton.addEventListener("click", function () {
      // Clear the timer when manually submitted
      clearInterval(timer);
    });
  }
});
