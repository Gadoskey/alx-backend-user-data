#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv('AUTH_TYPE')


# Set up auth based on environment variable
if auth_type == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """Filters and validates requests before processing them"""
    if auth is None:
        return
    # List of paths that don't require authorization
    excluded = [
            '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    # Check if the request path requires authentication
    if not auth.require_auth(request.path, excluded):
        return

    # Check if authorization header is provided
    if auth.authorization_header(request) is None:
        abort(401)  # Unauthorized

    # Check if a valid user is returned
    if auth.current_user(request) is None:
        abort(403)  # Forbidden


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """ Custom handler for 401 Unauthorized """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ Unauthorized error handler """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
