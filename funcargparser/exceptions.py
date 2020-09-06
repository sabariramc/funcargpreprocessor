#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Sep-2020
"""


class BadArgError(Exception):

    def __init__(self, message, data=None):
        self.data = data
        super(BadArgError, self).__init__(message)
