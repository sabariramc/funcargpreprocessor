#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Sep-2020
"""

from datetime import datetime, date
from decimal import Decimal


class BaseArg:
    def __init__(self, data_type):
        self.name = data_type

    def __call__(self, value):
        raise NotImplementedError

    def __repr__(self):
        return str(self.name)


class DateTimeArg(BaseArg):
    def __init__(self, fmt_string):
        self.fmt_string = fmt_string
        super().__init__(data_type=datetime)

    def __call__(self, value):
        if value is None:
            return datetime.now()
        return datetime.strptime(value, self.fmt_string)

    def __repr__(self):
        return f"{self.name} and format {self.fmt_string}"


class DateArg(BaseArg):
    def __init__(self, fmt_string):
        self.fmt_string = fmt_string
        super().__init__(data_type=date)

    def __call__(self, value=None):
        if value is None:
            return date.today()
        return datetime.strptime(value, self.fmt_string).date()

    def __repr__(self):
        return f"{str(self.name)} and format {self.fmt_string}"


class DecimalArg(BaseArg):
    def __init__(self):
        super().__init__(data_type=Decimal)

    def __call__(self, value=None):
        if value is None:
            return Decimal(0)
        return Decimal(str(value))


class FileArg(BaseArg):
    def __init__(self, mime_type=None, mime_list=None):
        self.mime_type = mime_type
        self.mime_list = mime_list
        super().__init__(data_type="File Stream Object")

    def __call__(self, file_mime_type):
        if self.mime_type:
            if file_mime_type.startswith(self.mime_type) is False:
                raise Exception()
        else:
            if file_mime_type not in self.mime_list:
                raise Exception()
        return file_mime_type

    def __repr__(self):
        if self.mime_type:
            return f"{str(self.name)} and mime type should be '{self.mime_type}'"
        super(FileArg, self).__repr__()
