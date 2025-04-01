from flask import Blueprint, request, jsonify
from bson import ObjectId

from utils import secure
from db import score_collection

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

    # Check if user is authenticated
    user = request.user
    if not user:
        return jsonify({"error": "Unauthorized"}), 401  # Unauthorized response

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
    table_score = {
        "quiz1 aptitude score ": apti_score,
        "quiz2 communication score ": comni_score,
        "quiz3 technical score ": technical_score,
        "compitency score ": (total_compitency / 10),
    }

    return jsonify(table_score), 200
