#!/usr/bin/env python3
"""auth.py"""
from flask import request
from typing import List, TypeVar
import fnmatch


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
        # Check each excluded path
        for excluded_path in excluded_paths:
            # If the excluded path ends with '*', use fnmatch
            if excluded_path.endswith('*'):
                if fnmatch.fnmatch(path, excluded_path):
                    return False
            # Otherwise, check for exact match
            elif path == excluded_path:
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
