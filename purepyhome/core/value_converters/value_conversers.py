from purepyhome.core.logger import get_logger

logger = get_logger()

VALID_DATA_CONVERTERS = ['str_to_bool']

def str_to_bool(value: str, info: dict) -> bool:

    # check if value is of type str
    if not isinstance(value, str):
        raise ValueError(f'Value {value} not of type str')
    
    # check if info dict provides the necessary information ('true' and 'false' keys)
    if 'true' not in info or 'false' not in info:
        raise ValueError(f'Info dict does not provide the necessary information (true and false keys)')
    
    # check if the keys are of type str
    if not isinstance(info['true'], str) or not isinstance(info['false'], str):
        raise ValueError(f'Info dict keys true and false not of type str')
    
    # convert the string to bool
    if value.lower() == info['true'].lower():
        return True
    elif value.lower() == info['false'].lower():
        return False
    else:
        raise ValueError(f'Value {value} not convertible to bool with true: {info["true"]} and false: {info["false"]}')

def str_to_bool_reverse(value: bool, info: dict) -> str:
    
    # check if value is of type bool
    if not isinstance(value, bool):
        raise ValueError(f'Value {value} not of type bool')
    
    # check if info dict provides the necessary information ('true' and 'false' keys)
    if 'true' not in info or 'false' not in info:
        raise ValueError(f'Info dict does not provide the necessary information (true and false keys)')
    
    # check if the keys are of type str
    if not isinstance(info['true'], str) or not isinstance(info['false'], str):
        raise ValueError(f'Info dict keys true and false not of type str')
    
    # convert the bool to string
    if value:
        return info['true']
    else:
        return info['false']



def run_value_converter(value: any, converter: str, info: dict, reverse: bool = False) -> any:
    if converter == "none":
        return value

    if converter not in VALID_DATA_CONVERTERS:
        raise ValueError(f'Converter {converter} not in {VALID_DATA_CONVERTERS}')
    
    if converter == 'str_to_bool':
        if reverse:
            logger.debug(f'str_to_bool - Converting {value} to str with info {info}')
            return str_to_bool_reverse(value, info)
        else:
            logger.debug(f'str_to_bool - Converting {value} to bool with info {info}')
            return str_to_bool(value, info)
    else:
        raise ValueError(f'Converter {converter} not implemented')
    