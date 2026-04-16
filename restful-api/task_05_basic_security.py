#!/usr/bin/python3
"""basic security api with basic auth and jwt auth."""

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-key"

auth = HTTPBasicAuth()
jwt = JWTManager(app)

users = {
    "user1": {
        "username": "user1",
        "password": generate_password_hash("password"),
        "role": "user"
    },
    "admin1": {
        "username": "admin1",
        "password": generate_password_hash("password"),
        "role": "admin"
    }
}


@auth.verify_password
def verify_password(username, password):
    """verify basic auth credentials."""
    user = users.get(username)
    if user and check_password_hash(user.get("password"), password):
        return username
    return None


@jwt.unauthorized_loader
def unauthorized_error(err):
    """handle missing token."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def invalid_token_error(err):
    """handle invalid token."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def expired_token_error(jwt_header, jwt_payload):
    """handle expired token."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def revoked_token_error(jwt_header, jwt_payload):
    """handle revoked token."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_error(jwt_header, jwt_payload):
    """handle fresh token required."""
    return jsonify({"error": "Fresh token required"}), 401


@app.route("/basic-protected", methods=["GET"])
@auth.login_required
def basic_protected():
    """basic auth protected route."""
    return "Basic Auth: Access Granted"


@app.route("/login", methods=["POST"])
def login():
    """login and return jwt token."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if not user or not check_password_hash(user.get("password"), password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity=user.get("username"),
        additional_claims={"role": user.get("role")}
    )
    return jsonify({"access_token": access_token})


@app.route("/jwt-protected", methods=["GET"])
@jwt_required()
def jwt_protected():
    """jwt protected route."""
    return "JWT Auth: Access Granted"


@app.route("/admin-only", methods=["GET"])
@jwt_required()
def admin_only():
    """admin only route."""
    username = get_jwt_identity()
    user = users.get(username)

    if user.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return "Admin Access: Granted"


if __name__ == "__main__":
    app.run()
