#!/usr/bin/env python3
""" Auth module
    Author: Yusuf Mustapha Opeyemi
"""
import bcrypt
from typing import List, Union


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
