#!/usr/bin/python3
"""simple flask api with in memory users."""
from flask import Flask, jsonify, request


app = Flask(__name__)
users = {}


@app.route("/")
def home():
    """return home message."""
    return "Welcome to the Flask API!"


@app.route("/status")
def status():
    """return api status."""
    return "OK"


@app.route("/data")
def data():
    """return all usernames."""
    return jsonify(list(users.keys()))


@app.route("/users/<username>")
def get_user(username):
    """return a user by username."""
    user = users.get(username)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@app.route("/add_user", methods=["POST"])
def add_user():
    """add a user from json payload."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    if users.get(username) is not None:
        return jsonify({"error": "Username already exists"}), 409

    users[username] = data
    return jsonify({"message": "User added", "user": data}), 201


if __name__ == "__main__":
    app.run()
