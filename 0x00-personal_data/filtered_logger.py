#!/usr/bin/python3
"""
Author: Gadoskey
Description: This module contains a function `filter_datum` that returns a log message obfuscated.
"""
import logging
import re
from typing import List


def filter_datum(self, fields: List[str], redaction: str, message: str, separator: str):
    """ filter_datum that returns a log message obfuscated """
    return re.sub(r'(' + '|'.join([f'{field}=[^;]*' for field in fields]) + ')',
                  lambda m: m.group(0).split('=')[0] + '=' + redaction, message)
