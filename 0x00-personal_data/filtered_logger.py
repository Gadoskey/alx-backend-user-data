#!/usr/bin/env python3
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
    # Function filter_datum that returns the log message obfuscated
    for f in fields:
        msg = re.sub(
           f'{f}=.*?{separator}', f'{f}={redaction}{separator}', message)
    return msg
