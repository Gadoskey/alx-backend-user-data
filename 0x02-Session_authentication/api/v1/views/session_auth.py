#!/usr/bin/env python3
"""
Session authentication routes.
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """
    Handles the POST /auth_session/login route for Session Authentication.

    Returns:
        JSON response with the User's details if authenticated successfully,
        otherwise error responses for various failure cases.
    """
    # Retrieve email and password from the request
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for a user with the given email
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate the user's password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session for the user
    session_id = auth.create_session(user.id)
    if not session_id:
        abort(500)  # Something went wrong with session creation

    # Prepare the response
    response = jsonify(user.to_json())

    # Set the session cookie
    session_name = getenv('SESSION_NAME')
    if not session_name:
        abort(500)  # SESSION_NAME environment variable not set

    response.set_cookie(session_name, session_id)

    return response
