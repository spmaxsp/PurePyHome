from purepyhome.core.data_types import ENTITY_DATA_TYPES

import colorsys
import re

def hsl_to_rgb(hsl: str) -> str:
    """Converts HSL to RGB color format.
            e.g. hsl(120, 100, 50) -> rgb(0,255,0)
    
    Args:
        hsl (str): HSL color format string
    
    Returns:
        str: RGB color format tuple
    """

    hsl_values = hsl.strip('hsl()').split(',')
    h, s, l = int(hsl_values[0]), int(hsl_values[1]) / 100, int(hsl_values[2]) / 100
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return (r, g, b)


def rgb_to_rgb(rgb: str) -> str:
    """Converts RGB to RGB color format. (just for consistency)
            e.g. rgb(0,255,0) -> rgb(0,255,0)

    Args:
        rgb (str): RGB color format string
    Returns:
        str: RGB color format tuple
    """

    rgb_values = rgb.strip('rgb()').split(',')
    r, g, b = int(rgb_values[0]), int(rgb_values[1]), int(rgb_values[2])

    return (r, g, b)


def hex_to_rgb(hex):
    """Converts HEX to RGB color format.
            e.g. #00ff00 -> (0, 255, 0)

    Args:
        hex (str): HEX color format string
    Returns:
        tuple: RGB color format tuple
    """

    hex = hex.lstrip('#')

    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def color_str_to_rgb_tuple(color: str) -> tuple:
    """Detects the color format and converts it to RGB (tuple).
            current formats supported:
                "20,10,250" -> (20,10,250)
                hsl(120, 100, 50) -> (0,255,0)
                rgb(0,255,0) -> (0,255,0)
                #00ff00 -> rgb(0,255,0)

        If the color format is not recognized, a ValueError is raised.

    Args:
        color (str): Color format string
    Returns:
        str: RGB color format string
    """

    if color.startswith("hsl("):
        return hsl_to_rgb(color)
    elif color.startswith("rgb("):
        return rgb_to_rgb(color)
    elif re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        return hex_to_rgb(color)
    elif re.match(r'^\d{1,3},\d{1,3},\d{1,3}$', color):
        return tuple(int(x) for x in color.split(','))
    else:
        raise ValueError(f'Color format {color} not recognized')


def check_and_correct_datatype(value, type):
    """Checks if the value has the correct datatype and corrects it if needed and possible.

    Args:
        value (any): The value to check
        type (str): The type of the value
    Returns:
        value (any): The corrected value
    """

    if value is None:
        return None
    
    if type not in ENTITY_DATA_TYPES:
        raise ValueError(f'Type {type} not in {ENTITY_DATA_TYPES}')
    
    if type == 'string':
        # correct type
        if isinstance(value, str):
            return value
        
        # try converting
        return str(value)
    
    elif type == 'numeric':
        # correct type
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return value
        
        # try converting
        if isinstance(value, str):
            return float(value)
        
        # else raise error
        raise ValueError(f'Value {value} not of type numeric and cannot be converted')
    
    elif type == 'bool':
        # correct type
        if isinstance(value, bool):
            return value
        
        # try converting
        if isinstance(value, str):
            return value.lower() in ['true', '1', 't', 'y', 'yes']
        if isinstance(value, int):
            return value == 1
        
        # else raise error
        raise ValueError(f'Value {value} not of type bool and cannot be converted')
    
    elif type == 'color':
        # correct type
        if isinstance(value, tuple) and len(value) == 3 and all(isinstance(x, int) for x in value):
            return value
        
        # try converting
        if isinstance(value, str):
            return color_str_to_rgb_tuple(value)
        
        # else raise error
        raise ValueError(f'Value {value} not of type color and cannot be converted')
    
    elif type == 'time':
        raise NotImplementedError('Time type not implemented')
    
    else:
        raise ValueError(f'Type {type} not implemented')