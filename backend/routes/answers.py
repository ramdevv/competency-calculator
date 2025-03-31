from flask import Blueprint, request, json, jsonify
import google.generativeai as genai
import os

from utils import secure
from db import score_collection

ans_bp = Blueprint("ans", __name__)

# Configure the Gemini API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


@ans_bp.route("/aptitude", methods=["POST"])
@secure
def get_aptianswers():
    print("🔥 /api/get_aptianswers endpoint hit!")
    new_data = request.get_json()

    new_prompt = f"""
       I will provide you with a set of 10 multiple-choice aptitude questions, the user's selected answers, and their corresponding marks/scores for each question. Your task is to:
        
        1.  **Rate the user's overall aptitude on a scale of 1 to 10**, where 1 indicates very low aptitude in problem-solving and cognitive abilities relevant to a technical role, and 10 indicates very high aptitude.


        Please present your analysis in a clear and structured format."      
        - Summarize the user's **personality type** in a clear and concise format.
        - Ensure the response is in **pure JSON format** without markdown or code blocks.
        ## **Example Output Format:**
        {{
            "aptitude_rating": 8,
            "analysis": [
                {{
                    "question": "Which number logically completes the following sequence: 2, 6, 12, 20, ?",
                    "user_answer": "30",
                    "interpretation": "Correct"
                }},
                {{
                    "question": "If 'TABLE' is coded as 'UBAMD,' then how is 'CHAIR' coded?",
                    "user_answer": "BSIAHQ",
                    "interpretation": "Incorrect"
                }},
                {{
                    "question": "A train travels 120 kilometers in 2 hours. How far will it travel in 5 hours at the same speed?",
                    "user_answer": "300 km",
                    "interpretation": "Correct"
                }}
            ],
            "summary": "The user demonstrates strong logical and numerical reasoning, but shows some weakness in abstract pattern identification. Overall aptitude is rated 8/10."
        }}

        Ensure the response is in pure JSON format without markdown or code blocks."

        Now, analyze the following data and generate a JSON response:
        

        {new_data}
        """
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    new_response = model.generate_content(new_prompt)

    response_text = new_response.text.strip()  # converts into string
    response_text = (
        response_text.replace("```json", "").replace("```", "").strip()
    )  # cleans the response_text
    response_dict = json.loads(response_text)

    user = request.user
    score = response_dict["aptitude_rating"]
    print(user)

    quiz_score_apti = score_collection.insert_one({"username": user, "score": score})

    print(quiz_score_apti)

    return jsonify(response_dict)


@ans_bp.route("/communications", methods=["POST"])
@secure
def get_comnianswers():
    new_data = request.get_json()

    new_prompt = f"""
        
        You are an expert in communication assessment. You will be provided with a set of 10 multiple-choice questions designed to evaluate a candidate's communication skills, along with the candidate's answers to those questions.
        The questions cover the following areas: Clarity and Conciseness, Active Listening, Written Communication, Verbal Communication, Interpretation of Non-Verbal Cues, Adaptability in Communication, Conflict Resolution through Communication, Professional Email/Message Etiquette, Understanding and Following Instructions, and Summarization and Paraphrasing.
        For each answer, assess its accuracy and appropriateness in relation to the skill being tested.
        Based on the overall performance across all 10 questions, provide a numerical score out of 10 for the candidate's communication skills.
        Following the numerical score, provide a concise overview of the candidate's communication skills, highlighting their strengths and areas where they may need to improve. Be specific and provide examples where possible, based on their given answers.
        Ensure to provide feedback on the candidates ability to communicate clearly, effectively, and professionally.


        Ensure the response is in pure JSON format without markdown or code blocks."

        Now, analyze the following data and generate a JSON response:
        

        {new_data}
        """
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    new_response = model.generate_content(new_prompt)

    response_text = new_response.text.strip()  # converts into string
    response_text = (
        response_text.replace("```json", "").replace("```", "").strip()
    )  # cleans the response_text
    response_text = response_text.replace("\n", " ")
    response_dict = json.loads(response_text)
    print(response_dict)

    user = request.user
    score = response_dict["score"]
    print(user)

    quiz_score_apti = score_collection.insert_one({"username": user, "score": score})

    print(quiz_score_apti)

    return jsonify(response_dict)


@ans_bp.route("/technical", methods=["POST"])
@secure
def get_technical_answers():

    new_data = request.get_json()

    new_prompt = f"""
            
            You are an expert in communication assessment. You will be provided with a set of 10 multiple-choice questions designed to evaluate a candidate's communication skills, along with the candidate's answers to those questions.
            The questions cover the following areas: Clarity and Conciseness, Active Listening, Written Communication, Verbal Communication, Interpretation of Non-Verbal Cues, Adaptability in Communication, Conflict Resolution through Communication, Professional Email/Message Etiquette, Understanding and Following Instructions, and Summarization and Paraphrasing.
            For each answer, assess its accuracy and appropriateness in relation to the skill being tested.
            Based on the overall performance across all 10 questions, provide a numerical score out of 10 for the candidate's communication skills.
            Following the numerical score, provide a concise overview of the candidate's communication skills, highlighting their strengths and areas where they may need to improve. Be specific and provide examples where possible, based on their given answers.
            Ensure to provide feedback on the candidates ability to communicate clearly, effectively, and professionally.


            Ensure the response is in pure JSON format without markdown or code blocks."

            Now, analyze the following data and generate a JSON response:
            

            {new_data}
            """
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    new_response = model.generate_content(new_prompt)

    response_text = new_response.text.strip()  # converts into string
    response_text = (
        response_text.replace("```json", "").replace("```", "").strip()
    )  # cleans the response_text
    response_dict = json.loads(response_text)
    print(response_dict)

    user = request.user
    score = response_dict["score"]
    print(user)

    technical_score_apti = score_collection.insert_one(
        {"username": user, "score": score}
    )

    print(technical_score_apti)

    return jsonify(response_dict)
