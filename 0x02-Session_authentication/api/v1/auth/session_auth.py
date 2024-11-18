#!/usr/bin/env python3
"""session_auth.py
  Author: Yusuf Mustapha Opeyemi
"""

import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Class SessionAuth that inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The ID of the user for whom the session is created.

        Returns:
            str: The Session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.

        Args:
            session_id (str): The session ID created for the user.

        Returns:
            str: User ID based on a Session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
          Returns a User instance based on a cookie value.

          Args:
              request: The incoming HTTP request.

          Returns:
              User: A User instance if the session is valid, otherwise None.
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        # Fetch and return the User instance using the user ID
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session / logs out.

        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was successfully destroyed, otherwise False.
        """
        if request is None:
            return False

        # Retrieve the session ID from the request cookie
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        # Check if the session ID is linked to a user ID
        if not self.user_id_for_session_id(session_id):
            return False

        # Delete the session ID from the user_id_by_session_id dictionary
        del self.user_id_by_session_id[session_id]

        return True
