#!/usr/bin/python3
"""
Author: Gadoskey
Description: This module contains a function `filter_datum` that returns a log message obfuscated.
"""
import logging
import re


def filter_datum(self, fields: list[str], redaction: str, message: str, seperator: str):
    """ filter_datum that returns a log message obfuscated """
    return re.sub(r'(' + '|'.join([f'{field}=[^;]*' for field in fields]) + ')',
                  lambda m: m.group(0).split('=')[0] + '=' + redaction, message)