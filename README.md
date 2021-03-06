# Function Argument Pre-Processor

This is a abstract library that need to be extended before put actual use.

The primary use case is to extend it as a `Flask Extenstion` but is open to use with any other environment/framework that needs to deal with http endpoints eg: `AWS Lambda`   

## Implementations
   [flask_requestpreprocesser](https://github.com/sabariramc/flask_requestpreprocesser)
   
## Installation

```bash
 $ pip install funcargpreprocessor
```

or download the code and run

```bash
 $ python3 setup.py install
```

## What it does?

 - Extraction and transformation of function argument and raise appropriate exceptions

## Example
 - Please refer [testimplementation.py](https://github.com/sabariramc/funcargpreprocessor/blob/master/testimplementation.py) and [fieldtest.py](https://github.com/sabariramc/funcargpreprocessor/blob/master/fieldtest.py) for examples
 
### Explanation

The following explanantion uses the example from `test` folder

```python

def get_current_time():
    return datetime.now().replace(microsecond=0)

def get_current_date():
    return date.today()

def get_future_date(date_factor=1):
    def inner_fu():
        return date.today() + timedelta(date_factor)

    return inner_fu


from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    TRANSGENDER = "transgender"

definition = {
    "pageNo": { #Key name expected from the HTTP endpoint
            "data_type": int # Data type expected   
            , "min_val": 0 # Min validation for the key 
            , "max_val": 20 # Max validation for the key
            , 'alias': 'page_no' # Key for the function argument, to the function the argument will be 'page_no'
                                 # Need? most of the time the http request are expected json and the keys will be in camelCase
            , "default": 1 # Default value for the field if no value has been passed
    }
    , "start_date": {
                "data_type": DateArg('%Y-%m-%d') # Expects a date argument in <str>'YYYY-MM-DD' format or datetime.date object accepts '2020-01-10', datetime.date(2020, 1, 10)  converts,in case of a string argument, to datetime.date(2020, 1, 10) and passes it to the function
                , "min_val": get_current_date # Function can be passed for min value, this function should not take any argument and should return a single value of the same type
                , "max_val": get_future_date(10) # Function can be passed for max value, this function should not take any argument and should return a single value of the same type
                , "required": True # This key is required to be there in the input
    }
    , "id_list": {
                "data_type": list # Expects list of value
                , "nested": int # The values in the list should be int same rule as `date_type`
                , "value_list": [0, 1, 2, 3] # Accepted values, valid argument ex: [1,2], [1], [2,3,0]
                                             # Need? Multiselect options
    }
    , "gender": {"data_type": str, "value_list": Gender} #Enum can be used for the value list and will be marshalled
    , "random_flag": {"data_type": int, "value_list": [0,1]} 
    , 'reg_time': {"data_type": DateTimeArg('%Y-%m-%d %H:%M:%S'), 
                    "default": get_current_time # Function can be passed for default value, this function should not take any argument and should return a single value of the same type
    }
    , "location": {"data_type": list
        , "nested": { # Custom definition for objects in the list
            "address_line_1": {"data_type": str, "required": True}
            , "address_line_2": {"data_type": str
                                    , "min_len": 5 #Mininum length expected for the argument
                                    , "max_len": 10 # Maximum length accepted for the argument
                                }
            , "latitude": {"data_type": DecimalArg(), "min_val": Decimal("-90"), "max_val": Decimal("90")}
            , "longitude": {"data_type": DecimalArg(), "min_val": Decimal("-180"), "max_val": Decimal("180")}
            , "pincode": {"data_type": int, "required": True}
            , "contact_person": {
                    "data_type": dict
                    , "nested": {
                        "first_name": {"data_type": str, "required": True}
                        , "last_name": {"data_type": str}
                        , "phone_number": {
                                    "data_type": str
                                    , "required": True
                                    , "regex": r"[0-9]{10,12}" # Regular expression validation
                                    , "regex_error_message": "<some message>" # Message when the RegEx validation fails 
                                }
                    }
            }   
        }
    }

}


```  
