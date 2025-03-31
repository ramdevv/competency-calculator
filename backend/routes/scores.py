from flask import Blueprint, request, jsonify, session
from bson import ObjectId

from utils import secure
from db import score_collection, user_collection

score_bp = Blueprint("score", __name__)


@score_bp.route("/evaluation", methods=["GET"])
@secure
def evaluation():
    user = request.user

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fetch all scores for the user
    user_scores = list(score_collection.find({"username": user}, {"_id": 0}))
    print(user_scores)
    apti_score = user_scores[0]["score"]
    comni_score = user_scores[0]["score"]
    technical_score = user_scores[0]["score"]
    total_competency = (50 * technical_score) + (30 * apti_score) + (20 * comni_score)

    table_score = {
        "quiz1 aptitude score ": apti_score,
        "quiz2 communication score ": comni_score,
        "quiz3 technical score ": technical_score,
        "compitency score ": (total_competency / 10),
    }

    if not user_scores:
        return jsonify({"message": "No scores found for this user"}), 404

    return jsonify(table_score)


@score_bp.route("/dashboard", methods=["GET"])
@secure
def get_dasboard_data():

    # Check if user is authenticated
    user = request.user
    if not user:
        return jsonify({"error": "Unauthorized"}), 401  # Unauthorized response

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
    table_score = {
        "quiz1 aptitude score ": apti_score,
        "quiz2 communication score ": comni_score,
        "quiz3 technical score ": technical_score,
        "compitency score ": (total_compitency / 10),
    }

    return jsonify(table_score), 200
