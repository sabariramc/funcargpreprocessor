#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Sep-2020
"""

from .errorcode import ErrorCode


class FieldError(Exception):

    def __init__(self, error_code, field_name, message, error_data=None):
        super().__init__(message)
        self.error_code = error_code
        self.field_name = field_name
        self.error_data = error_data
        self.message = message

    def __repr__(self):
        return f'{self.__class__}({self.error_code}, {self.field_name}, {self.message}, {self.error_data})'


class MissingFieldError(FieldError):

    def __init__(self, field_name):
        super().__init__(ErrorCode.MISSING_MANDATORY_FIELD, field_name, f'{field_name} is a mandatory field')


class FieldTypeError(FieldError):

    def __init__(self, field_name, data_type):
        super().__init__(ErrorCode.ERRONEOUS_FIELD_TYPE, field_name, f"{field_name} should be of type {data_type}",
                         {"expectedType": f'{data_type}'})


class FieldValueError(FieldError):
    pass
