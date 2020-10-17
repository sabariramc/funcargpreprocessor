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
{
    "pageNo": { #Key name expected from the HTTP endpoint
            "data_type": int # Data type expected, accepts 1, '1', 1.0 all of these values will be type casted to 1 before passing to the function   
            , "min_val": 0 # Min validation for the key 
            , "max_val": 20 # Max validation for the key
            , 'alias': 'page_no' # Key for the function argument, to the function the argument will be 'page_no'
                                 # Need? most of the time the http request are expected json and the keys will be in camelCase
    }
    , "start_date": {
                "data_type": DateArg('%Y-%m-%d') # Expects a date argument in <str>'YYYY-MM-DD' format or datetime.date object accepts '2020-01-10', datetime.date(2020, 1, 10)  converts,in case of a string argument, to datetime.date(2020, 1, 10) and passes it to the function
                , "min_val": date(2020, 1, 1)
                , "required": True # This key is required to be there in the input
    }
    , "id_list": {
                "data_type": list # Expects list of value
                , "nested": int # The values in the list should be int same rule as `date_type`
                , "value_list": [0, 1, 2, 3] # Accepted values ex: [1,2], [1], [2,3,0]
                                             # Need? Multiselect options/ENUMS
    }
    , 'reg_time': {"data_type": DateTimeArg('%Y-%m-%d %H:%M:%S')}
    , "location": {"data_type": list
        , "nested": { # Custom definition for objects in the list
            "address_line_1": {"data_type": str, "required": True}
            , "address_line_2": {"data_type": str}
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
