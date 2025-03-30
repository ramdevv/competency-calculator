const button = document.getElementById("button_id");
const container = document.getElementById("ques_content_id");
const submitbutton = document.getElementById("submit_id");

// Function to convert JSON into MCQ format
function displayMCQs(data) {
  container.innerHTML = ""; // Clear previous content

  if (!data.questions || !Array.isArray(data.questions)) {
    container.textContent = "Invalid question format received!";
    return;
  }

  // Loop through each question
  data.questions.forEach((q, index) => {
    const questionElement = document.createElement("p");
    questionElement.textContent = `${index + 1}. ${q.question}`;
    container.appendChild(questionElement);

    // Create radio buttons for each option
    q.options.forEach((option, optIndex) => {
      const optionWrapper = document.createElement("div");

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
      container.appendChild(optionWrapper);
    });

    container.appendChild(document.createElement("br"));
  });
}

// Event listener for fetching and displaying questions
var received_questions = "";
button.addEventListener("click", async () => {
  const job_profile_input = document.getElementById("job_profile_id").value;

  try {
    const response = await fetch(
      "http://localhost/api/get_technical_questions",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ job_profile: job_profile_input }),
      }
    );

    received_questions = await response.json(); // Parse JSON response

    console.log("Received Questions:", received_questions);

    displayMCQs(received_questions); //  Call function to format & display MCQs
  } catch (error) {
    console.error("Error fetching questions:", error);
    container.textContent = "Failed to load questions!";
  }
});

// function to ittereate through the questions
function collect_answers() {
  const answers = {};
  const questionElement = document.querySelectorAll("[name^='question_']");

  questionElement.forEach((element) => {
    if (element.checked) {
      const element_name = element.name; // to get the index of the questions

      const question_index = element.name.split("_")[1]; //  element.name gives -> "question_0", it converts it into ["question","0"] it removes the _

      const question_value = element.value; // this returns the vlue of the radio question

      answers[question_index] = question_value;
    }
  });
  console.log("the answers are :", answers); // this is to log the answers

  return answers;
}
// function to send the request to the backend
async function send_request(questions, answers) {
  try {
    console.log("i am inside the sendrequest function");
    const full_response = {
      questions: questions,
      answers: answers,
    };

    const new_response = await fetch(
      "http://localhost/api/get_technical_answers",
      {
        method: "POST",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify(full_response),
      }
    );
    if (!new_response.ok) {
      throw new Error(`HTTP error! Status: ${new_response.status}`); // if there is any issue with the response
    }

    // retrieve the data
    const response_data = await new_response.json();
    console.log("message sent to backend sucesfully :", response_data);
  } catch (error) {
    console.error("error sending the questions : ", error);
  }
}

// add the button listener to litsen ands run both the functions after it is clicked

submitbutton.addEventListener("click", async () => {
  console.log(" the button is pressed ");
  const user_answers = collect_answers(); // function to collect the answers
  send_request(received_questions, user_answers); // to send the user answers to the backend
});

const new_submitbutton = document.getElementById("new_submit_id");

new_submitbutton.addEventListener("click", async () => {
  console.log("the new button was pressed");
  window.location.href = "./evaluation.html";
});
