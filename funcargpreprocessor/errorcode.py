#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 15-Oct-2020
"""

from enum import Enum


class ErrorCode(Enum):
    MISSING_MANDATORY_FIELD = 1000
    ERRONEOUS_FIELD_TYPE = 1100
    UN_RECOGNIZED_FIELD = 1200
    FIELD_VALUE_ERROR = 1300
    FIELD_VALUE_EMPTY = 1301
    FIELD_MIN_RANGE_VIOLATED = 1310
    FIELD_MIN_LENGTH_VIOLATED = 1311
    FIELD_MAX_RANGE_VIOLATED = 1315
    FIELD_MAX_LENGTH_VIOLATED = 1316
    FIELD_VALUE_NOT_IN_ALLOWED_LIST = 1320
    FIELD_REGEX_VALIDATION_FAILED = 1330
