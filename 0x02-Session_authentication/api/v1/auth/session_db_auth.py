#!/usr/bin/env python3
"""session_db_auth.py
    Author: Yusuf Mustapha Opeyemi
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class for handling session storage in the database"""

    def create_session(self, user_id=None):
        """
        Create a session and store it in the database.

        Args:
            user_id (str): User ID for whom the session is created.

        Returns:
            str: The Session ID created, or None if it cannot be created.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save the session to the database
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the User ID associated with a session ID from the database.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: User ID if session is valid, otherwise None.
        """
        if session_id is None:
            return None

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None

        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy the session associated with the Session ID from the request.

        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was destroyed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()  # Remove the session from the database
        return True
