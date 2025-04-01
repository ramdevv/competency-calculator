const button = document.getElementById("button_id");
const container = document.getElementById("ques_content_id");
const submitButton = document.getElementById("submit_id");
const competencyButton = document.getElementById("new_submit_id");
const startSection = document.getElementById("start-section");

// Hide submit and competency buttons initially
submitButton.classList.add("hidden");
competencyButton.classList.add("hidden");

// Function to convert JSON into MCQ format
function displayMCQs(data) {
  container.innerHTML = ""; // Clear previous content

  if (!data.questions || !Array.isArray(data.questions)) {
    container.textContent = "Invalid question format received!";
    return;
  }

  // Loop through each question
  data.questions.forEach((q, index) => {
    const questionBox = document.createElement("div");
    questionBox.className = "question-box";

    const questionElement = document.createElement("p");
    questionElement.textContent = `${index + 1}. ${q.question}`;
    questionBox.appendChild(questionElement);

    // Create radio buttons for each option
    q.options.forEach((option, optIndex) => {
      const optionWrapper = document.createElement("div");
      optionWrapper.className = "option-wrapper";

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
      questionBox.appendChild(optionWrapper);
    });

    container.appendChild(questionBox);
  });
}

// Event listener for fetching and displaying questions
var received_questions = "";
button.addEventListener("click", async () => {
  const job_profile_input = document.getElementById("job_profile_id").value;

  if (!job_profile_input.trim()) {
    alert("Please enter a job profile before starting the quiz.");
    return;
  }

  try {
    const response = await fetch("/api/questions/technical", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ job_profile: job_profile_input }),
    });

    received_questions = await response.json(); // Parse JSON response

    console.log("Received Questions:", received_questions);

    // Hide start section (input field and start button)
    startSection.style.display = "none";

    // Display questions
    displayMCQs(received_questions);

    // Show submit button only
    submitButton.classList.remove("hidden");
    competencyButton.classList.add("hidden");
  } catch (error) {
    console.error("Error fetching questions:", error);
    container.textContent = "Failed to load questions!";
  }
});

// Function to iterate through the questions and collect answers
function collect_answers() {
  const answers = {};
  const questionElements = document.querySelectorAll("[name^='question_']");

  questionElements.forEach((element) => {
    if (element.checked) {
      const question_index = element.name.split("_")[1];
      const question_value = element.value;
      answers[question_index] = question_value;
    }
  });
  console.log("The answers are:", answers);

  return answers;
}
let insertid = null;
// Function to send the request to the backend
async function send_request(questions, answers) {
  try {
    console.log("I am inside the sendrequest function");
    const full_response = {
      questions: questions,
      answers: answers,
      insert_id: localStorage.getItem("insert_id"),
    };

    const new_response = await fetch("/api/answers/technical", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify(full_response),
    });

    if (!new_response.ok) {
      throw new Error(`HTTP error! Status: ${new_response.status}`);
    }

    // Retrieve the data
    const response_data = await new_response.json();
    console.log("Message sent to backend successfully:", response_data);
    return true;
  } catch (error) {
    console.error("Error sending the questions:", error);
    return false;
  }
}

// Add the button listener to listen and run both functions after it is clicked
submitButton.addEventListener("click", async () => {
  console.log("The submit button is pressed");

  const user_answers = collect_answers(); // Function to collect the answers

  // Check if user has answered all questions
  const totalQuestions = received_questions.questions
    ? received_questions.questions.length
    : 0;
  const answeredQuestions = Object.keys(user_answers).length;

  if (answeredQuestions < totalQuestions) {
    alert(
      `Please answer all questions. You've answered ${answeredQuestions} out of ${totalQuestions} questions.`
    );
    return;
  }

  const success = await send_request(received_questions, user_answers);
  console.log("submitted bhai");

  if (success) {
    console.log("we're inside the if");
    // Hide the submit button
    submitButton.classList.add("hidden");

    // Show the competency score button only
    competencyButton.classList.remove("hidden");
  }
});
console.log(insertid);
competencyButton.addEventListener("click", async () => {
  console.log("The competency button was pressed");

  // Redirect to the next page (optional)
  window.location.href = "./evaluation.html";
});
