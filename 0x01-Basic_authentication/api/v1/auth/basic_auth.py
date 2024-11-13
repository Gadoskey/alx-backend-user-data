#!/usr/bin/env python3
"""basic_auth.py"""

import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Class BasicAuth """
    pass