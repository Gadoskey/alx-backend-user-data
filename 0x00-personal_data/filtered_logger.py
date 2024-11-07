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
    # T
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                f'{f}={redaction}{separator}', message)
    return message
