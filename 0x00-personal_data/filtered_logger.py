#!/usr/bin/python3
"""
Author: Gadoskey
Description: This module contains a function `filter_datum`
that returns a log message obfuscated.
"""
import logging
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    p = r'(' + '|'.join([f'{field}=[^;]*' for field in fields]) + ')'
    return re.sub(
            p, lambda m: m.group(0).split('=')[0] + '=' + redaction, message)
