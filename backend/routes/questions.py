from flask import Blueprint, request, json, jsonify
import google.generativeai as genai
import os
from utils import secure

ques_bp = Blueprint("ques", __name__)

# Configure the Gemini API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


@ques_bp.route("/aptitude", methods=["GET"])
@secure
def get_aptitude():
    print(request.user)
    prompt = """
        Generate 10 multiple-choice aptitude questions designed to assess a candidate's cognitive abilities. Cover the following areas: logical reasoning, numerical reasoning, and verbal reasoning. Each question must have 4 distinct answer choices. Ensure the questions vary in difficulty and cover a range of problem-solving skills relevant to a technical role. 
        Each question should have 4 distinct answer choices.
        Output the result in **pure JSON format** without any code block formatting.

        Example:
        {
          "questions": [
            {
              "question": "Your question here?",
              "options": ["Option A", "Option B", "Option C", "Option D"]
            }
          ]
        }
    """

    print("Sending request to Gemini API...")
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    response = model.generate_content(prompt)

    raw_text = response.text.strip()
    # print("Raw API Response:", raw_text)  #  Debugging log

    # Remove unwanted Markdown formatting
    cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        questions_json = json.loads(cleaned_text)
        # print("Parsed JSON:", questions_json)  # Debugging log
        return jsonify(questions_json)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return (
            jsonify(
                {"error": "Invalid JSON response from API", "raw_response": raw_text}
            ),
            500,
        )


@ques_bp.route("/communications", methods=["GET"])
@secure
def get_communication():
    prompt = """
            Okay, here's a prompt designed to generate 10 multiple-choice aptitude questions for assessing a candidate's communication skills:
                
                "You are an expert in communication assessment. Generate 10 multiple-choice questions designed to evaluate a candidate's communication skills. Cover the following areas:
                Clarity and Conciseness: Ability to express ideas effectively and efficiently.
                Active Listening: Comprehension and retention of information from spoken or written sources.
                Written Communication: Grammar, spelling, tone, and organization in written messages.
                Verbal Communication: Articulation, tone, and appropriateness in spoken interactions.
                Interpretation of Non-Verbal Cues: Understanding and responding to body language and facial expressions.
                Adaptability in Communication: Tailoring communication style to different audiences and situations.
                Conflict Resolution through Communication: Handling disagreements and finding common ground.
                Professional Email/Message Etiquette: Following conventions for formal and informal digital communication.
                Understanding and Following Instructions: Accurately processing and acting upon directions.
                Summarization and Paraphrasing: Ability to condense and rephrase information accurately.
                Each question must have 4 distinct answer choices. Ensure the questions vary in difficulty and cover a range of communication skills relevant to a professional role. Provide the question followed by the 4 answer choices. Do not provide the answer key."
            Output the result in **pure JSON format** without any code block formatting.

            Example:
            {
            "questions": [
                {
                "question": "Your question here?",
                "options": ["Option A", "Option B", "Option C", "Option D"]
                }
            ]
            }
        """

    print("Sending request to Gemini API...")

    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    # Remove unwanted Markdown formatting
    cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        questions_json = json.loads(cleaned_text)
        print("Parsed JSON:", questions_json)  # Debugging log
        return jsonify(questions_json)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return (
            jsonify(
                {"error": "Invalid JSON response from API", "raw_response": raw_text}
            ),
            500,
        )


@ques_bp.route("/technical", methods=["POST"])
@secure
def get_technical_questions():
    data = request.get_json()
    job_profile = data.get("job_profile", "software engenner")
    prompt = f"""
    "You are an expert in technical assessment. You will be provided with a job profile description. Based on this job profile, generate 10 multiple-choice technical questions designed to assess the candidate's relevant skills and knowledge.
    The questions should be specific to the technologies, concepts, and practices typically required for the provided job profile.
    The questions should vary in difficulty, covering foundational to advanced concepts.
    Each question must have 4 distinct answer choices.
    Ensure the questions are relevant to the practical application of technical skills in the given job role.
    Focus on core technical competency that is required for the specified job.
    After the questions have been generated, please do not provide the answer key. Only provide the questions with the multiple choice answers.
    For example: If the job description is "Software Engineer - Python Backend", the questions should be related to Python, backend development, APIs, databases, etc.
    Here is the job profile: {job_profile}
    Provide the question followed by the 4 answer choices. Do not provide the answer key."
    Output the result in **pure JSON format** without any code block formatting.

    Example:
    {{
    "questions": [
        {{
        "question": "Your question here?",
        "options": ["Option A", "Option B", "Option C", "Option D"]
        }}
    ]
    }}
"""

    print("Sending request to Gemini API...")

    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    response = model.generate_content(prompt)

    raw_text = response.text.strip()
    print("Raw API Response:", raw_text)  # Debugging log

    # Remove unwanted Markdown formatting
    cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        questions_json = json.loads(cleaned_text)
        print("Parsed JSON:", questions_json)  # Debugging log
        return jsonify(questions_json)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return (
            jsonify(
                {"error": "Invalid JSON response from API", "raw_response": raw_text}
            ),
            500,
        )
