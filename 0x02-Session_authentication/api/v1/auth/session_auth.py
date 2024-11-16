#!/usr/bin/env python3
"""session_auth.py"""

import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Class SessionAuth that inherits from Auth """