#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 04-Jun-2020
"""

from datetime import date, datetime
from pprint import pprint
from copy import deepcopy
from uuid import uuid4, UUID

from classmethodimplemenation import parse_function_args
from funcargpreprocessor import DateArg, DateTimeArg, FieldError, ErrorCode
from funcargpreprocessor import FieldTypeError, FieldError, MissingFieldError

import unittest


def validate_uuid4(key, value):
    try:
        value = UUID(value, version=4)
    except Exception:
        raise FieldError(ErrorCode.ERRONEOUS_FIELD_TYPE, key, f'{key} should be UUID4')
    return str(value)


function_arg_definition = {
    "pageNo": {"data_type": int, "min_val": 1, "max_val": 10, 'alias': 'page_no'}
    , "start_date": {"data_type": DateArg('%Y-%m-%d'), "min_val": date(2020, 1, 1)}
    , "id_list": {"data_type": list, "nested": int,
                  "value_list": [0, 1, 2, 3]}
    , 'reg_time': {"data_type": DateTimeArg('%Y-%m-%d %H:%M:%S')}
    , 'request_id': {'validator': validate_uuid4, 'required': True}
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
    def test(self, fun_arg, *, start_date=None, location=None, id_list=None, **others):
        return {
            'start_date': start_date
            , 'location': location
            , 'id_list': id_list
            , **others
        }


class_instance = Test()


class FunctionArgTestCases(unittest.TestCase):
    def test_positive(self):
        start_date = date.today()
        reg_time = datetime.now()
        reg_time = reg_time.replace(microsecond=0)
        request_uuid = str(uuid4())
        location_1 = {"address_line_1": "fad", "pincode": 123124, "contact_person": {
            "first_name": "sabari"
            , "phone_number": "8884233317"
        }}
        location_2 = {"address_line_1": "fad", "pincode": 6544554, "contact_person": {
            "first_name": "sabari"
            , "phone_number": "8884233317"
        }}
        response = class_instance.test(
            {"start_date": start_date.strftime('%Y-%m-%d')
                , "reg_time": reg_time.strftime('%Y-%m-%d %H:%M:%S'),
             'request_id': request_uuid,
             "id_list": ["1", 1, 2, "0"],
             "location": [{**deepcopy(location_1), 'fad': 'fad'}, deepcopy(location_2)]}
        )
        self.assertEqual(response.get('start_date'), start_date)
        self.assertEqual(response.get('request_id'), request_uuid)
        self.assertEqual(response.get('reg_time'), reg_time)
        self.assertEqual(response.get('id_list'), [1, 1, 2, 0])
        self.assertEqual(response.get('location')[0], location_1)
        self.assertEqual(response.get('location')[1], location_2)

    def test_mandatory_error(self):
        with self.assertRaises(MissingFieldError) as e:
            class_instance.test({})
        self.assertEqual(e.exception.error_code, ErrorCode.MISSING_MANDATORY_FIELD)
        self.assertEqual(e.exception.field_name, 'request_id')
        self.assertEqual(e.exception.message, 'request_id is a mandatory field')

    def


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

if __name__ == '__main__':
    unittest.main()
