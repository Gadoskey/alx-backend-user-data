#!/usr/bin/env python3
"""user_session.py
    Author: Yusuf Mustapha Opeyemi
"""

from models.base import Base


class UserSession(Base):
    """UserSession model that handles user sessions in the database"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
