from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import get_user_by_token


from routes.auth import auth_bp
from routes.answers import ans_bp
from routes.questions import ques_bp
from routes.scores import score_bp


app = Flask(__name__)
app.secret_key = os.urandom(24)  # this will generate a randome secret key
CORS(app)
app.config["SESSION_TYPE"] = "mongodb"

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(ans_bp, url_prefix="/api/answers")
app.register_blueprint(score_bp, url_prefix="/api/scores")
app.register_blueprint(ques_bp, url_prefix="/api/questions")


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
