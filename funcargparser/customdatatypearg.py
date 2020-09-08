#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Sep-2020
"""

from datetime import datetime, date
from decimal import Decimal
from abc import ABC, abstractmethod

from .exceptions import TypeCastError


class BaseArg(ABC):
    def __init__(self, data_type):
        self.data_type = data_type

    def __call__(self, value):
        raise NotImplementedError

    def __repr__(self):
        return str(self.data_type)

    @abstractmethod
    def get_sample(self):
        pass


class DateTimeArg(BaseArg):
    def __init__(self, fmt_string):
        self.fmt_string = fmt_string
        super().__init__(data_type=datetime)

    def __call__(self, value):
        return datetime.strptime(value, self.fmt_string)

    def __repr__(self):
        return f"{self.data_type} and format {self.fmt_string}"

    def get_sample(self):
        return datetime.now()


class DateArg(BaseArg):
    def __init__(self, fmt_string):
        self.fmt_string = fmt_string
        super().__init__(data_type=date)

    def __call__(self, value):
        return datetime.strptime(value, self.fmt_string).date()

    def __repr__(self):
        return f"{str(self.data_type)} and format {self.fmt_string}"

    def get_sample(self):
        return datetime.now()


class DecimalArg(BaseArg):
    def __init__(self):
        super().__init__(data_type=Decimal)

    def __call__(self, value=None):
        return Decimal(str(value))

    def get_sample(self):
        return Decimal('0')


class FileArg(BaseArg):
    def __init__(self, mime_type=None, mime_list=None):
        self.mime_type = mime_type
        self.mime_list = mime_list
        super().__init__(data_type="File Stream Object")

    def __call__(self, file_mime_type):
        if self.mime_type:
            if file_mime_type.startswith(self.mime_type) is False:
                raise TypeCastError()
        else:
            if file_mime_type not in self.mime_list:
                raise TypeCastError()
        return file_mime_type

    def __repr__(self):
        if self.mime_type:
            return f"{str(self.data_type)} and mime type should be '{self.mime_type}'"
        return super().__repr__()

    def get_sample(self):
        raise NotImplementedError
