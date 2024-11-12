from flask import request
from typing import List, TypeVar

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that determines if authentication is required """
        return False


    def authorization_header(self, request=None) -> str:
        """ Method that returns authorization header """
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns the current user """
        return None
