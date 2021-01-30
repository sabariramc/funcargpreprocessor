#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 12-Sep-2020
"""

from funcargpreprocessor import FunctionArgPreProcessor


class FuncArgParser(FunctionArgPreProcessor):

    def extract_request_data(self, *args, **kwargs):
        return args[1]


def parse_function_args(query_param_definition, is_strict=False):
    def inner_get_fu(fu):
        return FuncArgParser(query_param_definition, is_strict=is_strict)(fu)

    return inner_get_fu


def parse_function_args_with_auto_type_cast(query_param_definition, is_strict=False):
    def inner_get_fu(fu):
        return FuncArgParser(query_param_definition, is_strict=is_strict, auto_type_cast=True)(fu)

    return inner_get_fu
