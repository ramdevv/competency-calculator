document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("button_id");
  const container = document.getElementById("ques_content_id");
  const submitbutton = document.getElementById("submit_id");

  if (!container) {
    console.error("Error: Element #ques_content_id not found in the DOM!");
    return;
  }

  function displayMCQs(data) {
    container.innerHTML = ""; // Clear previous content
    if (!data.questions || !Array.isArray(data.questions)) {
      container.textContent = "Invalid question format received!";
      return;
    }

    data.questions.forEach((q, index) => {
      const questionWrapper = document.createElement("div");
      questionWrapper.classList.add("question-box");

      const questionElement = document.createElement("p");
      questionElement.textContent = `${index + 1}. ${q.question}`;
      questionWrapper.appendChild(questionElement);

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

    button.classList.add("hidden");
    submitbutton.classList.remove("hidden");
  }

  var received_questions = "";

  button.addEventListener("click", async () => {
    try {
      const response = await fetch("/api/questions/communications", {
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
        insert_id: localStorage.getItem("insert_id"),
      };

      const new_response = await fetch("/api/answers/communications", {
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
      console.log("Message sent to backend successfully:", response_data);
    } catch (error) {
      console.error("Error sending the questions:", error);
    }
  }

  // Add the button listener to listen and run both functions after it is clicked
  submitbutton.addEventListener("click", async () => {
    console.log("The submit button is pressed");
    const user_answers = collect_answers();
    await send_request(received_questions, user_answers);
    console.log("shubham is gay");
    window.location.href = "technical.html";
  });
});
