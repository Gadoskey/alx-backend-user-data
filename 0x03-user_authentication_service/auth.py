#!/usr/bin/env python3
""" Auth module
    Author: Yusuf Mustapha Opeyemi
"""
import bcrypt
from typing import List, Union
from user import Base, User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
      Hashes a password using bcrypt.

      Args:
          password (str): The password to hash.

      Returns:
          bytes: The hashed password as bytes.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generates a new unique UUID.

    Returns:
        str: A string representation of the UUID.
    """
    new_uuid = uuid4()  # Generate a random UUID
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.

        Args:
            email (str): The user's email.
            password (str): The user's plaintext password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If the email is already associated with a user.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            # If no exception is raised, the user exists
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If NoResultFound is raised, the user does not exist
            hashed_password = _hash_password(password)
            # Add the user to the database
            new_user = self._db.add_user(
              email, hashed_password.decode("utf-8"))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login credentials.

        Args:
            email (str): The user's email.
            password (str): The user's plaintext password.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            # find the user by email
            user = self._db.find_user_by(email=email)
            # Verify the password against the hashed password
            if bcrypt.checkpw(
              password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                return True
        except Exception:
            # Handle cases where the user does not exist or other errors
            pass

        return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for a user.

        Args:
            email (str): The user's email.

        Returns:
            str: A new session ID for the user.
        """
        # find the user by email
        user = self._db.find_user_by(email=email)
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Finds a user with its session_id.

        Args:
            session_id (str): The session_id used to find the user.

        Returns:
            str: The user found or None if not found.
        """
        if session_id is None:
            return None
        # find the user by session_id
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            # If NoResultFound is raised, the user does not exist
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        Updates a user's session_id to none.

        Args:
            user_id (str): The user_id used to find the user.

        Returns:
            str: None.
        """
        # update user's session_id to None
        DB.update_user(user_id, session_id=None)
        return None
