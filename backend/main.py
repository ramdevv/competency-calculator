from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os


from .utils import get_user_by_token


# Configure the Gemini API key
genai.configure(api_key="AIzaSyAg009yAayCLFaRGfkf_MO6-5WMYsMS0-8")


app = Flask(__name__)
app.secret_key = os.urandom(24)  # this will generate a randome secret key
CORS(app)
app.config["SESSION_TYPE"] = "mongodb"


@app.route("/api/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/home", methods=["GET"])
def home():
    token = request.cookies.get("login_token")  # Get token from cookies
    if not get_user_by_token(token):
        return jsonify({"error": "Unauthorized"}), 401  # Return 401 for unauthorized

    return jsonify({"message": "Authorized"}), 200  # Return success message


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
