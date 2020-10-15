#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 04-Jun-2020
"""

from datetime import date, datetime
from pprint import pprint
from time import sleep

from classmethodimplemenation import parse_function_args
from funcargpreprocessor import DateArg, DateTimeArg

function_arg_definition = {
    "pageNo": {"data_type": int, "min_val": 1, 'alias': 'page_no'}
    , "start_date": {"data_type": DateArg('%Y-%m-%d'), "min_val": date(2020, 1, 1)}
    , "id_list": {"data_type": list, "nested": int,
                  "value_list": [0, 1, 2, 3]}
    , 'reg_time': {"data_type": DateTimeArg('%Y-%m-%d %H:%M:%S')}
    , "location": {"data_type": list
        , "nested": {
            "address_line_1": {"data_type": str, "required": True}
            , "address_line_2": {"data_type": str}
            , "pincode": {"data_type": int, "required": True}
            , "contact_person": {
                "data_type": dict, "nested": {
                    "first_name": {"data_type": str, "required": True}
                    , "last_name": {"data_type": str}
                    , "phone_number": {"data_type": str, "required": True, "regex": r"[0-9]{10,12}"}
                }
            }
        }
                   }
}


class Test:

    @parse_function_args(function_arg_definition)
    def test(self, org_arg, start_date=None, location=None, id_list=None, **others):
        pprint(id_list)
        pprint(start_date)
        pprint(location)
        pprint(others)


class_instance = Test()

class_instance.test(
    {"start_date": "2020-1-10", "reg_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "id_list": ["1", 1, 2, "0"],
     "location": [{"address_line_1": "fad", "pincode": 123124, "contact_person": {
         "first_name": "sabari"
         , "phone_number": "8884233317"
         , "fasdf": ''
     }}, {"address_line_1": "fad", "pincode": 6544554, "contact_person": {
         "first_name": "sabari"
         , "phone_number": "8884233317"
     }}]})

class_instance.test(
    {"pageNo": "3", "start_date": "2020-1-10", "reg_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
     "id_list": ["1", 1, 2, "0"],
     "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
         "first_name": "sabari"
         , "phone_number": "8884233317"
         , "fasdf": ''
     }}]})

try:
    class_instance.test(
        {"pageNo": "3", "start_date": "2020-1e-10", "reg_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         "id_list": ["1", 1, 2, "0"],
         "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
             "first_name": "sabari"
             , "phone_number": "8884233317"
             , "fasdf": ''
         }}]})
except Exception as e:
    pprint(e)

try:
    class_instance.test(
        {"pageNo": "a", "start_date": "2020-1-10", "reg_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         "id_list": ["1", 1, 2, "0"],
         "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
             "first_name": "sabari"
             , "phone_number": "8884233317"
             , "fasdf": ''
         }}]})
except Exception as e:
    pprint(e)

try:
    class_instance.test(
        {"pageNo": "1", "start_date": "2020-1-10", "reg_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         "id_list": ["1", 1, 2, "0"],
         "location": [{"address_line_1": "fad", "pincode": "XX", "contact_person": {
             "first_name": "sabari"
             , "phone_number": "8884233317"
             , "fasdf": ''
         }}]})
except Exception as e:
    pprint(e)

try:
    class_instance.test(
        {"pageNo": "2", "start_date": "2020-1-10", "reg_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         "id_list": ["1", 1, 2, "0"],
         "location": [{"address_line_1": "fad", "pincode": "636351", "contact_person": {
             "first_name": "sabari"
             , "phone_number": "AB"
             , "fasdf": ''
         }}]})
except Exception as e:
    print(e)
    pprint(e)
