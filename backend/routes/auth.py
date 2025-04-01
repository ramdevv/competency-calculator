from flask import Blueprint, request, session, jsonify, make_response
from werkzeug.security import check_password_hash
import random

from db import user_collection
from utils import create_user, get_user_by_name

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
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


@auth_bp.route("/login", methods=["POST"])
def login():

    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

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
    response.set_cookie("login_token", login_token)
    if user and check_password_hash(user["password"], password):
        session[username] = True
        return response
    return jsonify({"error": "the username and password are incorrect"}), 401


@auth_bp.route("/logout", methods=["POST"])
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
