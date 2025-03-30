from flask import Flask, request, jsonify, json, session, make_response
from flask_session import Session
from bson import ObjectId
from pymongo import MongoClient
from flask_cors import CORS
import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random


# Configure the Gemini API key
genai.configure(api_key="AIzaSyAg009yAayCLFaRGfkf_MO6-5WMYsMS0-8")


app = Flask(__name__)
app.secret_key = os.urandom(24)  # this will generate a randome secret key
app.config["SESSION_TYPE"] = "mongodb"
CORS(app)

# setting up the database
mongo_server = MongoClient("mongodb://localhost:27017")
ccc_db = mongo_server.ccc_database

user_collection = ccc_db.user
score_collection = ccc_db.score


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "the user has not logged in"})
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    username = user["username"]
    return username


def create_user(username, password):
    return user_collection.insert_one(
        {
            "username": username,
            "password": generate_password_hash(password),
            "analysis": [],
            "read_token": "".join(random.choice("0123456789ABCDEF") for i in range(16)),
            "login_token": "",
        }
    )


def get_user_by_name(username):
    return user_collection.find_one({"username": username})


def get_user_by_token(token):
    return user_collection.find_one({"login_token": token})


@app.route("/api/sign_in/", methods=["POST"])
def sign_in():

    print("Request received!")
    print(request.form)  # Prints all form data

    username = request.form.get("username")
    password = request.form.get("password")

    existing_user = user_collection.find_one({"username": username})

    # to check if the user is already in the databse table
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    new_user = create_user(username, password)  # this is the function

    session["user_id"] = str(new_user.inserted_id)  # Convert ObjectId to string
    session.modified = True  # Ensure session is updated
    print("User added successfully and session updated:", session["user_id"])

    return (
        jsonify(
            {"message": "User registered successfully!", "redirect": "/login.html"}
        ),
        201,
    )


@app.route("/api/login/", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")
    print(username)

    if not username or not password:
        return ({"error": "username and password are requeired"}), 400

    else:
        username = username.strip()  # this would remove the white spaces from the input
        password = password.strip()
        login_token = "".join(
            [random.choice("0123456789ABCDEF") for i in range(16)]
        )  # random value in the login token
        user_collection.update_one(
            {"username": username},
            {"$set": {"login_token": login_token}},
        )

        user = get_user_by_name(username)
        response = make_response(jsonify({"message": "login succesful"}), 200)
        response.set_cookie("login_token", login_token, httponly=True, secure=True)
        if user and check_password_hash(user["password"], password):
            session[username] = True
            return response
        return jsonify({"error": "the username and password are incorrect"}), 401


@app.route("/api/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/get_aptitude", methods=["GET"])
def get_aptitude():
    token = request.cookies.get("login_token")  # getting token
    if not get_user_by_token(token):
        return jsonify({"error": "unauthorized"}, 401)
    # Define the prompt
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

    # Call the Gemini API
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


@app.route("/api/get_aptianswers", methods=["POST"])
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

    user = get_current_user()
    score = response_dict["aptitude_rating"]
    print(user)

    quiz_score_apti = score_collection.insert_one({"username": user, "score": score})

    print(quiz_score_apti)

    return jsonify(response_dict)


@app.route("/api/get_communication", methods=["GET"])
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
    print("Raw API Response:", raw_text)  #  Debugging log

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


@app.route("/api/get_comnianswers", methods=["POST"])
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

    user = get_current_user()
    score = response_dict["score"]
    print(user)

    quiz_score_apti = score_collection.insert_one({"username": user, "score": score})

    print(quiz_score_apti)

    return jsonify(response_dict)


@app.route("/api/get_technical_questions", methods=["POST"])
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


@app.route("/api/get_technical_answers", methods=["POST"])
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

    user = get_current_user()
    score = response_dict["score"]
    print(user)

    technical_score_apti = score_collection.insert_one(
        {"username": user, "score": score}
    )

    print(technical_score_apti)

    return jsonify(response_dict)


@app.route("/api/home", methods=["GET"])
def home():
    token = request.cookies.get("login_token")  # Get token from cookies
    if not get_user_by_token(token):
        return jsonify({"error": "Unauthorized"}), 401  # Return 401 for unauthorized

    return jsonify({"message": "Authorized"}), 200  # Return success message


@app.route("/api/evaluation", methods=["GET"])
def evaluation():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    user = user_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "User not found"}), 404

    username = user["username"]

    # Fetch all scores for the user
    user_scores = list(score_collection.find({"username": username}, {"_id": 0}))
    print(user_scores)
    apti_score = user_scores[0]["score"]
    comni_score = user_scores[0]["score"]
    technical_score = user_scores[0]["score"]
    total_compitency = (50 * technical_score) + (30 * apti_score) + (20 * comni_score)

    print(total_compitency)

    if not user_scores:
        return jsonify({"message": "No scores found for this user"}), 404

    return jsonify(total_compitency)


@app.route("/api/logout/", methods=["POST"])
def logout():
    login_token = request.cookies.get("login_token")

    if not login_token:
        return jsonify({"error": "No token provided"}), 401

    # Get the current user using the login token
    user = user_collection.find_one({"login_token": login_token})

    if not user:
        return jsonify({"error": "Invalid token or user already logged out"}), 400

    username = user["username"]

    # Remove login token from the database
    result = user_collection.update_one(
        {"username": username}, {"$unset": {"login_token": ""}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Failed to logout"}), 400

    # Clear the cookie on the client-side
    response = jsonify({"message": "Logged out successfully"})
    response.set_cookie("login_token", "", expires=0, path="/")  # Expire the cookie

    return response


@app.route("/api/dashboard/", methods=["GET"])
def get_dasboard_data():

    if not get_user_by_token(request.cookies.get("login_token")):
        return jsonify({"error": "unauthorized"}, 401)
    user = get_user_by_token(request.cookies.get("login_token"))
    return


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
