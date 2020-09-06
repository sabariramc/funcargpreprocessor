#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 08-Jun-2020
"""

from functools import wraps
import re

from .exceptions import BadArgError
from .customdatatypearg import BaseArg


class FunctionArgParser:
    def __init__(self, definition, is_strict=True):
        self.is_strict = is_strict
        self.definition = self.validate_type_definition(definition)

    def __call__(self, func_obj):
        @wraps(func_obj)
        def role_checker(*args, **kwargs):
            raw_argument = self.extract_request_data(*args, **kwargs)
            parsed_argument = self.parser(raw_argument, self.definition)
            kwargs.update(parsed_argument)
            return func_obj(*args, **kwargs)

        return role_checker

    def extract_request_data(self, *args, **kwargs):
        return {}

    def parser(self, params, definition, parent=None):
        if self.is_non_empty_value(params) is False:
            params = {}
        validated_params = {}
        for key, type_def in definition.items():
            value = params.pop(key, None)
            required = type_def.pop("required", False)
            alias_key = type_def.pop('alias', key)
            data_type = type_def.pop('data_type')
            validator = type_def.pop('validator', None)
            child = type_def.pop('child', None)
            try:
                print_key = f"{parent}.{key}" if parent else key
                if self.is_non_empty_value(value):
                    validated_params[alias_key] = self.parse_value(print_key, value, data_type, validator, child,
                                                                   **type_def)
                elif required:
                    raise BadArgError(f"{print_key} should not be empty")
            finally:
                type_def["required"] = required
        if self.is_strict and self.is_non_empty_value(params):
            raise BadArgError(f'Unexpected params {list(params.keys())}')
        return validated_params

    @classmethod
    def parse_value(cls, key, value, data_type, validator, child, **value_constraints):
        if validator:
            value = validator(value)
        else:
            try:
                value = cls.type_cast(value, data_type)
            except Exception:
                raise BadArgError(f"{key} should be of type {data_type}")
        if child:
            if isinstance(child, dict):
                if data_type is dict:
                    value = cls.parser(value, child, key)
                elif data_type is list:
                    temp_list = []
                    for item in value:
                        list_item = cls.parser(item, child, key)
                        temp_list.append(list_item)
                    value = temp_list
            else:
                if data_type is not list:
                    raise BadArgError(f"{data_type} is not compatible for nested checks")
                for i, item in enumerate(value):
                    try:
                        list_item = cls.type_cast(item, child)
                        value[i] = list_item
                    except Exception:
                        raise BadArgError(f"{key} should be of {data_type} of {child}")
                    cls.check_constraint(list_item, key, **value_constraints)

        else:
            cls.check_constraint(value, key, **value_constraints)
        return value

    @staticmethod
    def check_constraint(value, key, min_val=None, max_val=None, value_list=None, regex=None,
                         regex_error_message=None):
        """
        To check the value for constraints. The caller of this function provides only the value and key as positional
        argument and others as keyword arguments so that the function can be changed as the developer needs by extending
        the class and overriding the function
        :param value: Value to be checked
        :param key: Key name for passing back in error if any constraint fails
        :param min_val: Min range constraint
        :param max_val: Max range constraint
        :param value_list: Pick list constraint
        :param regex: Regular expression constraint
        :param regex_error_message: Alternate error message for regex constraint fails
        :return:
        """
        if min_val and value < min_val:
            raise BadArgError(f"{key} should be greater than or equal to {min_val}")
        if max_val and value > max_val:
            raise BadArgError(f"{key} should be lesser than or equal to {max_val}")
        if value_list and value not in value_list:
            raise BadArgError(f"{key} should be one of these - {value_list}")
        if regex and re.search(regex, value) is None:
            if regex_error_message:
                raise BadArgError(f"{key} {regex_error_message}")
            else:
                raise BadArgError(f"{key} should be of format - {regex}")

    @staticmethod
    def validate_type_definition(type_definition):
        return type_definition

    @staticmethod
    def type_cast(value, data_type):
        """
        To check if the value is of expected data type if not type cast it to the required datatype. Supports type cast
        for BaseParams as well
        :param value: Value from the request
        :param data_type: Expected data type of the param
        :return: type casted value
        """
        if (isinstance(data_type, BaseArg) and isinstance(value, data_type.name) is False) or isinstance(value,
                                                                                                         data_type) is False:
            value = data_type(value)
        return value

    @staticmethod
    def is_non_empty_value(value):
        """
        To check if the value is not None and in case of string check for non empty string
        :param value: Any basic data type
        :return:Boolean
        """
        if value is None:
            return False
        if isinstance(value, str) and len(value.strip()) == 0:
            return False
        if (isinstance(value, list) or isinstance(value, dict)) and not value:
            return False
        return True
