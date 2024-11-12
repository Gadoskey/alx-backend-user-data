#!/usr/bin/env python3
"""auth.py"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class Auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that determines if authentication is required """
        if path is None:
          return True
        elif excluded_paths is None or len(excluded_paths) == 0:
          return True
        elif path in excluded_paths:
          return False
        return False

    def authorization_header(self, request=None) -> str:
        """ Method that returns authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns the current user """
        return None
