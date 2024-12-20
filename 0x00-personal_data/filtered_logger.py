#!/usr/bin/env python3
"""
Author: Gadoskey
Description: This module contains a function `filter_datum`
that returns a log message obfuscated.
"""
import logging
import re
import os
from typing import List
import mysql.connector
from mysql.connector import connection


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscate specified fields in the log message."""
    p = r'|'.join([f'{field}=.*?{separator}' for field in fields])
    return re.sub(p, lambda m: f"{m.group(0).split('=')[0]}={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """Creates and configures a logger named 'user_data'"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """Connects to the MySQL database using credentials from environment variables."""
    db_config = {
        'user': os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        'database': os.getenv('PERSONAL_DATA_DB_NAME')
    }
    return mysql.connector.connect(**db_config)
