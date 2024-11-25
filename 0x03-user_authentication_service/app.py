#!/usr/bin/env python3
""" Flask App
    Author: Yusuf Mustapha Opeyemi
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from db import DB
from sqlalchemy.orm.exc import NoResultFound


AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    POST /users
    Registers a new user.

    Returns:
        JSON response with appropriate message and status code.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    POST /sessions
    Login a user.

    Returns:
        JSON response with appropriate message and status code.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    DELETE /sessions
    Logout a user.

    Returns:
        JSON response with appropriate message and status code.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    try:
        user = AUTH._db.find_user_by(session_id=session_id)
        AUTH.destroy_session(user.id)
        return redirect(homepage)
    except NoResultFound:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """
    GET /profile
    Display a user.

    Returns:
        JSON response with appropriate message and status code.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    try:
        user = AUTH._db.find_user_by(session_id=session_id)
        email = (user.email)
        return jsonify({"email": email}), 200
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    POST /reset_password
    Reset a user's password.

    Returns:
        JSON response with appropriate message and status code.
    """
    email = request.form.get("email")
    if not email:
        abort(403)
    try:
        user = AUTH._db.find_user_by(email=email)
        reset_token = AUTH.get_reset_password_token
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
