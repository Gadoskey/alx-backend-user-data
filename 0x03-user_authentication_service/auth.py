#!/usr/bin/env python3
""" Auth module
    Author: Yusuf Mustapha Opeyemi
"""
import bcrypt
from typing import List, Union
from user import Base, User
from db import DB


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
        # Check if the user already exists
        new_user = self._db.find_user_by(email=email)
        if new_user:
            raise ValueError(f"User {email} already exists")
        # Hash the password
        hashed_password = _hash_password(password)
        # Add the user to the database
        new_user = self._db.add_user(email, hashed_password.decode('utf-8'))
        
        return new_user
