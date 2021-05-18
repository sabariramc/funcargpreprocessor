#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 04-Jun-2020
"""

from datetime import date, datetime, timedelta
from copy import deepcopy
from uuid import uuid4, UUID
from decimal import Decimal

from testimplementation import parse_function_args, parse_function_args_with_auto_type_cast
from funcargpreprocessor import DateArg, DateTimeArg, ErrorCode, DecimalArg
from funcargpreprocessor import FieldTypeError, FieldError, MissingFieldError, FieldValueError

import unittest


def validate_uuid4(key, value):
    try:
        value = UUID(value, version=4)
    except Exception:
        raise FieldError(ErrorCode.ERRONEOUS_FIELD_TYPE, key, f'{key} should be UUID4')
    return str(value)


def get_current_time():
    return datetime.now().replace(microsecond=0)


def get_current_date():
    return date.today()


def get_future_date(date_factor=1):
    def inner_fu():
        return date.today() + timedelta(days=date_factor)

    return inner_fu


from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    TRANSGENDER = "transgender"


function_arg_definition = {
    "pageNo": {"data_type": int, "min_val": 0, "max_val": 10, 'alias': 'page_no', "description": "Test description",
               "default": 1}
    , "start_date": {"data_type": DateArg('%Y-%m-%d'), "min_val": date.today, "max_val": get_future_date(10)}
    , "id_list": {"data_type": list, "nested": int,
                  "value_list": [0, 1, 2, 3]}
    , 'reg_time': {"data_type": DateTimeArg('%Y-%m-%d %H:%M:%S'), "default": get_current_time}
    , 'request_id': {'validator': validate_uuid4, 'required': True}
    , "name": {"data_type": dict, "nested": {
        "first_name": {"data_type": str}, "last_name": {"data_type": str}
    }}
    , "gender": {"data_type": str, "value_list": Gender}
    , "location": {"data_type": list
        , "nested": {
            "address_line_1": {"data_type": str, "required": True}
            , "address_line_2": {"data_type": str}
            , "pincode": {"data_type": int, "required": True}
            , "latitude": {"data_type": DecimalArg(), "min_val": Decimal("-90"), "max_val": Decimal("90")}
            , "longitude": {"data_type": DecimalArg(), "min_val": Decimal("-180"), "max_val": Decimal("180")}
            , "contact_person": {
                "data_type": dict, "nested": {
                    "first_name": {"data_type": str, "required": True, "min_len": 5, "max_len": 10}
                    , "last_name": {"data_type": str}
                    , "phone_number": {"data_type": str, "required": True, "regex": r"[0-9]{10,12}"}
                }
            }
        }

                   }
    , "location_check": {"data_type": bool}
}


class TestNonAutoCast:

    @parse_function_args(function_arg_definition)
    def test(self, fun_arg, **kwargs):
        return kwargs


not_auto_cast_class_instance = TestNonAutoCast()


class TestAutoCast:
    @parse_function_args_with_auto_type_cast(function_arg_definition)
    def test(self, fun_arg, **kwargs):
        return kwargs


auto_cast_class_instance = TestAutoCast()


class FunctionArgTestCases(unittest.TestCase):
    def test_positive_1(self):
        start_date = date.today()
        reg_time = datetime.now()
        reg_time = reg_time.replace(microsecond=0)
        request_uuid = str(uuid4())
        location_1 = {"address_line_1": "fad", "pincode": 123124, "contact_person": {
            "first_name": "sabari"
            , "phone_number": "8884233317"
        }}
        latitude = "-43.12412"
        location_2 = {"address_line_1": "fad"
            , "pincode": 6544554
            , "latitude": latitude
            , "contact_person": {
                "first_name": "sabari"
                , "phone_number": "8884233317"
            }}
        name = {
            "first_name": "Sabari"
        }
        gender = "male"
        response = not_auto_cast_class_instance.test(
            {
                "pageNo": 10, "start_date": start_date.strftime('%Y-%m-%d')
                , "reg_time": reg_time.strftime('%Y-%m-%d %H:%M:%S')
                , 'request_id': request_uuid
                , "id_list": [1, 1, 2, 0]
                , "location": [{**deepcopy(location_1), 'fad': 'fad'}, deepcopy(location_2)]
                , "name": deepcopy(name)
                , "location_check": True
                , "gender": gender
            }

        )
        location_2["latitude"] = Decimal(latitude)
        self.assertEqual(response.get('page_no'), 10)
        self.assertEqual(response.get('start_date'), start_date)
        self.assertEqual(response.get('request_id'), request_uuid)
        self.assertEqual(response.get('reg_time'), reg_time)
        self.assertEqual(response.get('id_list'), [1, 1, 2, 0])
        self.assertEqual(response.get('location')[0], location_1)
        self.assertEqual(response.get('location')[1], location_2)
        self.assertEqual(response.get('location')[1], location_2)
        self.assertEqual(response.get('name'), name)
        self.assertEqual(response.get('gender'), Gender(gender))
        self.assertEqual(response.get('location_check'), True)

    def test_positive_2(self):
        start_date = date.today()
        reg_time = datetime.now()
        reg_time = reg_time.replace(microsecond=0)
        request_uuid = str(uuid4())
        location_1 = {"address_line_1": "fad", "pincode": 123124, "contact_person": {
            "first_name": "sabari"
            , "phone_number": "8884233317"
        }}
        latitude = "-43.12412"
        location_2 = {"address_line_1": "fad"
            , "pincode": 6544554
            , "latitude": latitude
            , "contact_person": {
                "first_name": "sabari"
                , "phone_number": "8884233317"
            }}
        name = {
            "first_name": "Sabari"
        }
        response = not_auto_cast_class_instance.test(
            {
                "start_date": start_date.strftime('%Y-%m-%d'),
                'request_id': request_uuid,
                "id_list": [1, 1, 2, 0],
                "location": [{**deepcopy(location_1), 'fad': 'fad'}, deepcopy(location_2)]
                , "name": deepcopy(name)
                , "location_check": True
            }

        )
        location_2["latitude"] = Decimal(latitude)
        self.assertEqual(response.get('page_no'), 1)
        self.assertEqual(response.get('start_date'), start_date)
        self.assertEqual(response.get('request_id'), request_uuid)
        self.assertEqual(response.get('reg_time'), reg_time)
        self.assertEqual(response.get('id_list'), [1, 1, 2, 0])
        self.assertEqual(response.get('location')[0], location_1)
        self.assertEqual(response.get('location')[1], location_2)
        self.assertEqual(response.get('location')[1], location_2)
        self.assertEqual(response.get('name'), name)
        self.assertEqual(response.get('location_check'), True)

    def test_mandatory_error(self):
        with self.assertRaises(MissingFieldError) as e:
            not_auto_cast_class_instance.test({})
        self.assertEqual(e.exception.error_code, ErrorCode.MISSING_MANDATORY_FIELD)
        self.assertEqual(e.exception.field_name, 'request_id')
        self.assertEqual(e.exception.message, 'request_id is a mandatory field')

    def test_type_error_int(self):
        with self.assertRaises(FieldTypeError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 'a',
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('pageNo', e.exception.field_name)
        self.assertEqual(f'pageNo should be of type {int}', e.exception.message)
        self.assertEqual({"expectedType": f'{int}'}, e.exception.error_data)

    def test_type_error_nested_int(self):
        with self.assertRaises(FieldTypeError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 'id_list': [1, 'a'],
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('id_list[1]', e.exception.field_name)
        self.assertEqual(f'id_list[1] should be of type {int}', e.exception.message)
        self.assertEqual({"expectedType": f'{int}'}, e.exception.error_data)

    def test_type_error_datetime(self):
        with self.assertRaises(FieldTypeError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "start_date": "afsa",
                 'id_list': [1, 3],
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('start_date', e.exception.field_name)
        self.assertEqual('start_date should be of type {"type": "<class \'datetime.date\'>", "format": "%Y-%m-%d"}',
                         e.exception.message)
        self.assertEqual({'expectedType': '{"type": "<class \'datetime.date\'>", "format": "%Y-%m-%d"}'},
                         e.exception.error_data)

    def test_type_error_bool(self):
        with self.assertRaises(FieldTypeError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 'id_list': [1, 3],
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]
                    , "location_check": 1})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('location_check', e.exception.field_name)
        self.assertEqual("location_check should be of type <class 'bool'>", e.exception.message)
        self.assertEqual({'expectedType': "<class 'bool'>"}, e.exception.error_data)

    def test_value_error_value_list(self):
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 'id_list': [1, 4],
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_VALUE_NOT_IN_ALLOWED_LIST, e.exception.error_code)
        self.assertEqual('id_list[1]', e.exception.field_name)
        self.assertEqual(f'id_list[1] should be one of these - [0, 1, 2, 3]', e.exception.message)
        self.assertEqual({"allowedValue": [0, 1, 2, 3]}, e.exception.error_data)

    def test_value_error_min_value(self):
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': -1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MIN_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('pageNo', e.exception.field_name)
        self.assertEqual('pageNo should be greater than or equal to 0', e.exception.message)
        self.assertEqual({'minValue': 0}, e.exception.error_data)

    def test_value_error_max_value(self):
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 11,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MAX_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('pageNo', e.exception.field_name)
        self.assertEqual('pageNo should be lesser than or equal to 10', e.exception.message)
        self.assertEqual({'maxValue': 10}, e.exception.error_data)

    def test_value_error_min_value_1(self):
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "latitude": "-91", "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MIN_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('location[0].latitude', e.exception.field_name)
        self.assertEqual('location[0].latitude should be greater than or equal to -90', e.exception.message)
        self.assertEqual({'minValue': Decimal("-90")}, e.exception.error_data)

    def test_value_error_max_value_1(self):
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "latitude": "91", "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MAX_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('location[0].latitude', e.exception.field_name)
        self.assertEqual('location[0].latitude should be lesser than or equal to 90', e.exception.message)
        self.assertEqual({'maxValue': Decimal("90")}, e.exception.error_data)

    def test_value_error_max_value_2(self):
        start_date = (date.today() + timedelta(days=11)).strftime('%Y-%m-%d')
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 "start_date": start_date,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MAX_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('start_date', e.exception.field_name)
        self.assertEqual(f'start_date should be lesser than or equal to {date.today() + timedelta(days=10)}',
                         e.exception.message)
        self.assertEqual({'maxValue': date.today() + timedelta(days=10)}, e.exception.error_data)

    def test_length_error_1(self):
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "saba"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MIN_LENGTH_VIOLATED, e.exception.error_code)
        self.assertEqual('location[0].contact_person.first_name', e.exception.field_name)
        self.assertEqual('location[0].contact_person.first_name has a minimum length of 5', e.exception.message)
        self.assertEqual({'minLength': 5}, e.exception.error_data)

    def test_length_error_2(self):
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari fadsfasfasf"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MAX_LENGTH_VIOLATED, e.exception.error_code)
        self.assertEqual('location[0].contact_person.first_name', e.exception.field_name)
        self.assertEqual('location[0].contact_person.first_name has a maximum length of 10', e.exception.message)
        self.assertEqual({'maxLength': 10}, e.exception.error_data)

    def test_regex_error(self):
        with self.assertRaises(FieldValueError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "888423A3317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_REGEX_VALIDATION_FAILED, e.exception.error_code)
        self.assertEqual('location[0].contact_person.phone_number', e.exception.field_name)
        self.assertEqual('location[0].contact_person.phone_number should be of format - [0-9]{10,12}',
                         e.exception.message)

    def test_validator_error(self):
        with self.assertRaises(FieldError) as e:
            not_auto_cast_class_instance.test(
                {'request_id': 'fasdfsdaf',
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('request_id', e.exception.field_name)
        self.assertEqual('request_id should be UUID4', e.exception.message)

    def test_field_validation_list(self):
        with self.assertRaises(FieldTypeError) as e:
            not_auto_cast_class_instance.test({
                "request_id": str(uuid4())
                , "location": {"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                    "first_name": "sabari"
                    , "phone_number": "8884233317"
                }}
            })
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual("location", e.exception.field_name)
        self.assertEqual(e.exception.message, "location should be of type <class 'list'>")

    def test_field_validation_dict(self):
        with self.assertRaises(FieldTypeError) as e:
            not_auto_cast_class_instance.test({
                "request_id": str(uuid4())
                , "location": {"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                    "first_name": "sabari"
                    , "phone_number": "8884233317"
                }}
                , "name": "fasdf"
            })
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual("name", e.exception.field_name)
        self.assertEqual("name should be of type <class 'dict'>", e.exception.message)


class FunctionArgAutoTypeCastTestCases(unittest.TestCase):
    def test_positive_1(self):
        start_date = date.today()
        reg_time = datetime.now()
        reg_time = reg_time.replace(microsecond=0)
        request_uuid = str(uuid4())
        location_1 = {"address_line_1": "fad", "pincode": 123124, "contact_person": {
            "first_name": "sabari"
            , "phone_number": "8884233317"
        }}
        latitude = "-43.12412"
        location_2 = {
            "address_line_1": "fad"
            , "pincode": 6544554
            , "latitude": latitude
            , "contact_person": {
                "first_name": "sabari"
                , "phone_number": "8884233317"
            }
        }
        name = {
            "first_name": "Sabari"
        }
        gender = "female"
        response = auto_cast_class_instance.test({
            "pageNo": 10, "start_date": start_date.strftime('%Y-%m-%d')
            , "reg_time": reg_time.strftime('%Y-%m-%d %H:%M:%S')
            , 'request_id': request_uuid
            , "id_list": [1, 1, 2, 0]
            , "location": [{**deepcopy(location_1), 'fad': 'fad'}, deepcopy(location_2)]
            , "name": deepcopy(name)
            , "location_check": True
            , "gender": gender
        }

        )
        location_2["latitude"] = Decimal(latitude)
        self.assertEqual(response.get('page_no'), 10)
        self.assertEqual(response.get('start_date'), start_date)
        self.assertEqual(response.get('request_id'), request_uuid)
        self.assertEqual(response.get('reg_time'), reg_time)
        self.assertEqual(response.get('id_list'), [1, 1, 2, 0])
        self.assertEqual(response.get('location')[0], location_1)
        self.assertEqual(response.get('location')[1], location_2)
        self.assertEqual(response.get('location')[1], location_2)
        self.assertEqual(response.get('name'), name)
        self.assertEqual(response.get('gender'), Gender(gender))

    def test_positive_2(self):
        start_date = date.today()
        reg_time = datetime.now()
        reg_time = reg_time.replace(microsecond=0)
        request_uuid = str(uuid4())
        location_1 = {"address_line_1": "fad", "pincode": 123124, "contact_person": {
            "first_name": "sabari"
            , "phone_number": "8884233317"
        }}
        latitude = "-43.12412"
        location_2 = {
            "address_line_1": "fad"
            , "pincode": 6544554
            , "latitude": latitude
            , "contact_person": {
                "first_name": "sabari"
                , "phone_number": "8884233317"
            }
        }
        name = {
            "first_name": "Sabari"
        }
        page_no = "9"
        response = auto_cast_class_instance.test(
            {
                "pageNo": page_no,
                "start_date": start_date.strftime('%Y-%m-%d'),
                'request_id': request_uuid,
                "id_list": [1, 1, 2, 0],
                "location": [{**deepcopy(location_1), 'fad': 'fad'}, deepcopy(location_2)]
                , "name": deepcopy(name)
                , "location_check": "True"
            }

        )
        location_2["latitude"] = Decimal(latitude)
        self.assertEqual(response.get('page_no'), int(page_no))
        self.assertEqual(response.get('start_date'), start_date)
        self.assertEqual(response.get('request_id'), request_uuid)
        self.assertEqual(response.get('reg_time'), reg_time)
        self.assertEqual(response.get('id_list'), [1, 1, 2, 0])
        self.assertEqual(response.get('location')[0], location_1)
        self.assertEqual(response.get('location')[1], location_2)
        self.assertEqual(response.get('location')[1], location_2)
        self.assertEqual(response.get('name'), name)
        self.assertEqual(response.get('location_check'), True)

    def test_mandatory_error(self):
        with self.assertRaises(MissingFieldError) as e:
            auto_cast_class_instance.test({})
        self.assertEqual(e.exception.error_code, ErrorCode.MISSING_MANDATORY_FIELD)
        self.assertEqual(e.exception.field_name, 'request_id')
        self.assertEqual(e.exception.message, 'request_id is a mandatory field')

    def test_type_error_int(self):
        with self.assertRaises(FieldTypeError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 'a',
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('pageNo', e.exception.field_name)
        self.assertEqual(f'pageNo should be of type {int}', e.exception.message)
        self.assertEqual({"expectedType": f'{int}'}, e.exception.error_data)

    def test_type_error_nested_int(self):
        with self.assertRaises(FieldTypeError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': '1',
                 'id_list': [1, 'a'],
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('id_list[1]', e.exception.field_name)
        self.assertEqual(f'id_list[1] should be of type {int}', e.exception.message)
        self.assertEqual({"expectedType": f'{int}'}, e.exception.error_data)

    def test_type_error_datetime(self):
        with self.assertRaises(FieldTypeError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "start_date": "afsa",
                 'id_list': [1, 3],
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('start_date', e.exception.field_name)
        self.assertEqual('start_date should be of type {"type": "<class \'datetime.date\'>", "format": "%Y-%m-%d"}',
                         e.exception.message)
        self.assertEqual({'expectedType': '{"type": "<class \'datetime.date\'>", "format": "%Y-%m-%d"}'},
                         e.exception.error_data)

    def test_type_error_bool(self):
        with self.assertRaises(FieldTypeError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 'id_list': [1, 3],
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]
                    , "location_check": 1})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('location_check', e.exception.field_name)
        self.assertEqual("location_check should be of type <class 'bool'>", e.exception.message)
        self.assertEqual({'expectedType': "<class 'bool'>"}, e.exception.error_data)

    def test_value_error_value_list(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 'id_list': [1, 4],
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_VALUE_NOT_IN_ALLOWED_LIST, e.exception.error_code)
        self.assertEqual('id_list[1]', e.exception.field_name)
        self.assertEqual(f'id_list[1] should be one of these - [0, 1, 2, 3]', e.exception.message)
        self.assertEqual({"allowedValue": [0, 1, 2, 3]}, e.exception.error_data)

    def test_value_error_min_value(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': -1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MIN_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('pageNo', e.exception.field_name)
        self.assertEqual('pageNo should be greater than or equal to 0', e.exception.message)
        self.assertEqual({'minValue': 0}, e.exception.error_data)

    def test_value_error_max_value(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 11,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MAX_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('pageNo', e.exception.field_name)
        self.assertEqual('pageNo should be lesser than or equal to 10', e.exception.message)
        self.assertEqual({'maxValue': 10}, e.exception.error_data)

    def test_value_error_min_value_1(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "latitude": "-91", "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MIN_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('location[0].latitude', e.exception.field_name)
        self.assertEqual('location[0].latitude should be greater than or equal to -90', e.exception.message)
        self.assertEqual({'minValue': Decimal("-90")}, e.exception.error_data)

    def test_value_error_max_value_1(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "latitude": "91", "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MAX_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('location[0].latitude', e.exception.field_name)
        self.assertEqual('location[0].latitude should be lesser than or equal to 90', e.exception.message)
        self.assertEqual({'maxValue': Decimal("90")}, e.exception.error_data)

    def test_value_error_max_value_2(self):
        start_date = (date.today() + timedelta(days=11)).strftime('%Y-%m-%d')
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 "start_date": start_date,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MAX_RANGE_VIOLATED, e.exception.error_code)
        self.assertEqual('start_date', e.exception.field_name)
        self.assertEqual(f'start_date should be lesser than or equal to {date.today() + timedelta(days=10)}',
                         e.exception.message)
        self.assertEqual({'maxValue': date.today() + timedelta(days=10)}, e.exception.error_data)

    def test_length_error_1(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "location": [{"address_line_1": "fad", "pincode": "6544554", "contact_person": {
                     "first_name": "saba"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MIN_LENGTH_VIOLATED, e.exception.error_code)
        self.assertEqual('location[0].contact_person.first_name', e.exception.field_name)
        self.assertEqual('location[0].contact_person.first_name has a minimum length of 5', e.exception.message)
        self.assertEqual({'minLength': 5}, e.exception.error_data)

    def test_length_error_2(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 'pageNo': 1,
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari fadsfasfasf"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_MAX_LENGTH_VIOLATED, e.exception.error_code)
        self.assertEqual('location[0].contact_person.first_name', e.exception.field_name)
        self.assertEqual('location[0].contact_person.first_name has a maximum length of 10', e.exception.message)
        self.assertEqual({'maxLength': 10}, e.exception.error_data)

    def test_regex_error(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test(
                {'request_id': str(uuid4()),
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "888423A3317"
                 }}]})
        self.assertEqual(ErrorCode.FIELD_REGEX_VALIDATION_FAILED, e.exception.error_code)
        self.assertEqual('location[0].contact_person.phone_number', e.exception.field_name)
        self.assertEqual('location[0].contact_person.phone_number should be of format - [0-9]{10,12}',
                         e.exception.message)

    def test_validator_error(self):
        with self.assertRaises(FieldError) as e:
            auto_cast_class_instance.test(
                {'request_id': 'fasdfsdaf',
                 "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                     "first_name": "sabari"
                     , "phone_number": "8884233317"
                 }}]})
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual('request_id', e.exception.field_name)
        self.assertEqual('request_id should be UUID4', e.exception.message)

    def test_field_validation_list(self):
        with self.assertRaises(FieldTypeError) as e:
            auto_cast_class_instance.test({
                "request_id": str(uuid4())
                , "location": {"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                    "first_name": "sabari"
                    , "phone_number": "8884233317"
                }}
            })
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual("location", e.exception.field_name)
        self.assertEqual(e.exception.message, "location should be of type <class 'list'>")

    def test_field_validation_dict(self):
        with self.assertRaises(FieldTypeError) as e:
            auto_cast_class_instance.test({
                "request_id": str(uuid4())
                , "location": {"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                    "first_name": "sabari"
                    , "phone_number": "8884233317"
                }}
                , "name": "fasdf"
            })
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual("name", e.exception.field_name)
        self.assertEqual("name should be of type <class 'dict'>", e.exception.message)

    def test_cast_error(self):
        with self.assertRaises(FieldTypeError) as e:
            auto_cast_class_instance.test({
                "request_id": str(uuid4())
                , "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                    "first_name": "sabari"
                    , "phone_number": "8884233317"
                }}]
                , "name": "fasdf"
            })
        self.assertEqual(ErrorCode.ERRONEOUS_FIELD_TYPE, e.exception.error_code)
        self.assertEqual("name", e.exception.field_name)
        self.assertEqual("name should be of type <class 'dict'>", e.exception.message)

    def test_enum_error(self):
        with self.assertRaises(FieldValueError) as e:
            auto_cast_class_instance.test({
                "request_id": str(uuid4())
                , "location": [{"address_line_1": "fad", "pincode": 6544554, "contact_person": {
                    "first_name": "sabari"
                    , "phone_number": "8884233317"
                }}]
                , "gender": "fasdf"
            })
        self.assertEqual(ErrorCode.FIELD_VALUE_NOT_IN_ALLOWED_LIST, e.exception.error_code)
        self.assertEqual("gender", e.exception.field_name)
        self.assertEqual("gender should be one of these - ['male', 'female', 'transgender']", e.exception.message)


if __name__ == '__main__':
    unittest.main()
