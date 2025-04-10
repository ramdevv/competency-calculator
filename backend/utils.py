from bson import ObjectId
from werkzeug.security import generate_password_hash
from flask import jsonify, session, request, redirect
import random
from functools import wraps

from db import user_collection


def secure(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("login_token")
        request.user = user_collection.find_one({"login_token": token})
        if not request.user:
            return redirect("/login.html")
        return func(*args, **kwargs)

    return wrapper


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
    if not token:
        return token
    return user_collection.find_one({"login_token": token})
