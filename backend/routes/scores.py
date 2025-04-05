from flask import Blueprint, request, jsonify
from bson import ObjectId
import uuid

from utils import secure, get_user_by_token
from db import score_collection, scorecard_collection

score_bp = Blueprint("score", __name__)


@score_bp.route("/evaluation", methods=["POST"])
@secure
def evaluation():
    data = request.get_json()  # Get JSON data from request
    print("got the insert id")
    insert_id = data.get("insert_id")
    print(insert_id)
    if not insert_id:
        return jsonify({"error": "Insert ID not found in session"}), 400

    # Fetch the score using the insert_id
    user_scores = score_collection.find_one({"_id": ObjectId(insert_id)})
    print("user scores: ", user_scores)
    if not user_scores:
        return jsonify({"message": "No scores found for this user"}), 404

    print("there is nothing in user score")
    apti_score = user_scores["apti_score"]
    comni_score = user_scores["comni_score"]
    technical_score = user_scores["technical_score"]
    total_competency = (50 * technical_score) + (30 * apti_score) + (20 * comni_score)

    table_score = {
        "quiz1 aptitude score ": apti_score,
        "quiz2 communication score ": comni_score,
        "quiz3 technical score ": technical_score,
        "compitency score ": (total_competency / 10),
    }

    return jsonify(table_score)


@score_bp.route("/dashboard", methods=["GET"])
@secure
def get_dasboard_data():

    user = request.user

    user_scores_collections = score_collection.find({"username": user})

    user_scores = list(user_scores_collections)
    for item in user_scores_collections:
        print("askl;djfhaskl;djfasdl;", item)

    response_dict = []
    quiz_no = 0
    for scores in user_scores:

        apti_score = scores.get("apti_score", 0)
        comni_score = scores.get("comni_score", 0)
        technical_score = scores.get("technical_score", 0)
        total_competency = (
            (50 * technical_score) + (30 * apti_score) + (20 * comni_score)
        )

        table_entry = {
            "quiz_score": quiz_no,
            "quiz1 aptitude score ": apti_score,
            "quiz2 communication score ": comni_score,
            "quiz3 technical score ": technical_score,
            "compitency score ": (total_competency / 10),
        }
        response_dict.append(table_entry)
        quiz_no += 1

    return jsonify(response_dict)


@score_bp.route("/get_url", methods=["POST"])
@secure
def get_url():
    data = request.get_json()

    random_link = str(uuid.uuid4())[:16]
    link_content = {
        "random_id": random_link,
        "score_content": data,
    }
    scorecard_collection.insert_one(link_content)

    return jsonify({"link": f"http://localhost/yourscorecard/{random_link}"})
