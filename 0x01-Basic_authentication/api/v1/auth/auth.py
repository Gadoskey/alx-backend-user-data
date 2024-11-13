#!/usr/bin/env python3
"""auth.py"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class Auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that determines if authentication is required """
        # Return True if path is None
        if path is None:
            return True
        # Return True if excluded_paths is None or empty
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        # Normalize path by adding a trailing slash if it's not present
        if not path.endswith('/'):
            path += '/'
        # Return False if path is in excluded_paths
        if path in excluded_paths:
            return False
        # Otherwise, return True
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the Authorization header from the request"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns the current user """
        return None
