#!/usr/bin/env python3
"""session_exp_auth.py
    Author: Yusuf Mustapha Opeyemi
"""

import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class that inherits from SessionAuth"""

    def __init__(self):
        """Initialize the SessionExpAuth instance with session duration"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session ID and store additional session information.

        Args:
            user_id (str): User ID for whom the session is created.

        Returns:
            str: The Session ID created, or None if it cannot be created.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the User ID associated with a valid session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: User ID if session is valid, otherwise None.
        """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        user_id = session_data.get('user_id')
        created_at = session_data.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return user_id
