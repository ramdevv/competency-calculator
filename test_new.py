from flask import Flask, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


def get_current_user():
    """This function runs inside a request to get the current user."""
    if "user_id" not in session:
        return None
    return User.query.get(session["user_id"])


@app.route("/api/current_user", methods=["GET"])
def current_user_api():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not logged in"}), 401
    return jsonify({"user_id": user.user_id, "username": user.username})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
