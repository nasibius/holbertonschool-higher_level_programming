#!/usr/bin/python3
"""flask api with basic auth, jwt auth, and role-based access control"""

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-me"

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
    """verify basic auth username and password."""
    user = users.get(username)
    if user and check_password_hash(user.get("password"), password):
        return username
    return None


@auth.error_handler
def basic_auth_error(status):
    """return consistent unauthorized response for basic auth errors."""
    return jsonify({"error": "Unauthorized"}), 401


@jwt.unauthorized_loader
def handle_unauthorized_error(err):
    """handle missing token errors."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def handle_invalid_token_error(err):
    """handle invalid token errors."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def handle_expired_token_error(jwt_header, jwt_payload):
    """handle expired token errors."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def handle_revoked_token_error(jwt_header, jwt_payload):
    """handle revoked token errors."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def handle_needs_fresh_token_error(jwt_header, jwt_payload):
    """handle fresh token requirement errors"""
    return jsonify({"error": "Fresh token required"}), 401


@jwt.user_lookup_error_loader
def handle_user_lookup_error(jwt_header, jwt_payload):
    """handle user lookup errors"""
    return jsonify({"error": "Missing or invalid token"}), 401


@app.route("/basic-protected", methods=["GET"])
@auth.login_required
def basic_protected():
    """basic auth protected endpoint"""
    return jsonify("Basic Auth: Access Granted")


@app.route("/login", methods=["POST"])
def login():
    """authenticate user and return jwt token"""
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if not user or not check_password_hash(user.get("password"), password):
        return jsonify({"error": "Invalid credentials"}), 401

    identity = {"username": user.get("username"), "role": user.get("role")}
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token})


@app.route("/jwt-protected", methods=["GET"])
@jwt_required()
def jwt_protected():
    """jwt protected endpoint."""
    return jsonify("JWT Auth: Access Granted")


@app.route("/admin-only", methods=["GET"])
@jwt_required()
def admin_only():
    """admin role protected endpoint."""
    identity = get_jwt_identity()
    if identity.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return jsonify("Admin Access: Granted")


if __name__ == "__main__":
    app.run()