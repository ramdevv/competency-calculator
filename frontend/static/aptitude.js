const button = document.getElementById("button_id");
const container = document.getElementById("ques_content_id");
const submitbutton = document.getElementById("submit_id");

// Create loading spinner function
function createLoadingSpinner() {
  const spinnerContainer = document.createElement("div");
  spinnerContainer.className = "spinner-container";

  const spinner = document.createElement("div");
  spinner.className = "spinner";

  spinnerContainer.appendChild(spinner);
  return spinnerContainer;
}

function displayMCQs(data) {
  // Remove the loading spinner if it exists
  const existingSpinner = container.querySelector(".spinner-container");
  if (existingSpinner) {
    existingSpinner.remove();
  }

  container.innerHTML = ""; // Clear previous content

  if (!data.questions || !Array.isArray(data.questions)) {
    container.textContent = "Invalid question format received!";
    return;
  }

  // Loop through each question
  data.questions.forEach((q, index) => {
    const questionElement = document.createElement("p");
    questionElement.textContent = `${index + 1}. ${q.question}`;

    // Wrap questions in a div
    const questionWrapper = document.createElement("div");
    questionWrapper.classList.add("question-box");
    questionWrapper.appendChild(questionElement);

    // Create options
    q.options.forEach((option, optIndex) => {
      const optionWrapper = document.createElement("div");
      optionWrapper.classList.add("option-wrapper");

      const input = document.createElement("input");
      input.type = "radio";
      input.name = `question_${index}`;
      input.id = `q${index}_opt${optIndex}`;
      input.value = option;

      const label = document.createElement("label");
      label.htmlFor = `q${index}_opt${optIndex}`;
      label.textContent = option;

      optionWrapper.appendChild(input);
      optionWrapper.appendChild(label);
      questionWrapper.appendChild(optionWrapper);
    });

    container.appendChild(questionWrapper);
  });

  // Hide the start quiz button
  button.classList.add("hidden");

  // Show the submit button after questions are displayed
  submitbutton.classList.remove("hidden");
}

// Event listener for fetching and displaying questions
var received_questions = "";
button.addEventListener("click", async () => {
  try {
    // Show loading spinner
    button.disabled = true;
    button.textContent = "Loading...";

    // Add the spinner to the container
    container.innerHTML = "";
    container.appendChild(createLoadingSpinner());

    const response = await fetch("/api/questions/aptitude", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    received_questions = await response.json();
    console.log("Received Questions:", received_questions);
    displayMCQs(received_questions);
  } catch (error) {
    console.error("Error fetching questions:", error);
    container.textContent = "Failed to load questions!";
    button.disabled = false;
    button.textContent = "TRY AGAIN";
  }
});

// Function to iterate through the questions
function collect_answers() {
  const answers = {};
  const questionElements = document.querySelectorAll(
    "input[type='radio']:checked"
  );

  questionElements.forEach((element) => {
    const question_index = element.name.split("_")[1];
    const question_value = element.value;
    answers[question_index] = question_value;
  });

  console.log("The answers are:", answers);
  return answers;
}

// Function to send the request to the backend
async function send_request(questions, answers) {
  try {
    console.log("Inside the sendrequest function");
    const full_response = {
      questions: questions,
      answers: answers,
    };

    const new_response = await fetch("/api/answers/aptitude", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify(full_response),
    });

    if (!new_response.ok) {
      throw new Error(`HTTP error! Status: ${new_response.status}`);
    }

    const response_data = await new_response.json();
    localStorage.setItem("insert_id", response_data.apti_inserted_id);
    console.log("Message sent to backend successfully:", response_data);
    return true;
  } catch (error) {
    console.error("Error sending the questions:", error);
    return false;
  }
}

// Add the button listener to listen and run both functions after it is clicked
submitbutton.addEventListener("click", async () => {
  console.log("The submit button is pressed");

  // Show loading state
  submitbutton.disabled = true;
  const originalButtonText = submitbutton.value;
  submitbutton.value = "Submitting...";

  // Add spinner after the submit button
  const submitSpinner = createLoadingSpinner();
  submitbutton.parentNode.appendChild(submitSpinner);

  const user_answers = collect_answers();
  const success = await send_request(received_questions, user_answers);

  if (success) {
    window.location.href = "communication.html";
  } else {
    // Remove spinner and restore button if there was an error
    submitSpinner.remove();
    submitbutton.disabled = false;
    submitbutton.value = originalButtonText;
  }
});
