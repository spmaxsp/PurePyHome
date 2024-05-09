import colorsys
import re

def hsl_to_rgb(hsl: str) -> str:
    """Converts HSL to RGB color format.
            e.g. hsl(120, 100, 50) -> rgb(0,255,0)
    
    Args:
        hsl (str): HSL color format string
    
    Returns:
        str: RGB color format string
    """

    hsl_values = hsl.strip('hsl()').split(',')
    h, s, l = int(hsl_values[0]), int(hsl_values[1]) / 100, int(hsl_values[2]) / 100
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return f"rgb({r},{g},{b})"


def rgb_to_rgb(rgb: str) -> str:
    """Converts RGB to RGB color format. (just for consistency)
            e.g. rgb(0,255,0) -> rgb(0,255,0)

    Args:
        rgb (str): RGB color format string
    Returns:
        str: RGB color format string
    """

    return rgb


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


def detect_color_and_convert(color: str) -> str:
    """Detects the color format and converts it to RGB.
            e.g. #00ff00 -> rgb(0,255,0)
                or hsl(120, 100, 50) -> rgb(0,255,0)
                or rgb(0,255,0) -> rgb(0,255,0)
        If the color format is not recognized, returns False.

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
    else:
        return False


def get_nested_value(obj: dict, key: str) -> any:
    """Get a nested value from a dictionary using a dot-separated key.
        The value can be multiple levels deep in the dictionary.
            eg. get_nested_value({'a': {'b': {'c': 1}}}, 'a.b.c') -> 1

    Args:
        obj (dict): The dictionary to search in
        key (str): The dot-separated key to search for
    Returns:
        any: The value found in the dictionary, or None if not found
    """

    keys = key.split('.')
    try:
        value = obj
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return None


def nest_data_to_object(key: str, value: any) -> dict:
    """Nest a value in a dictionary using a dot-separated key.
        The value can be multiple levels deep in the dictionary.
            eg. nest_data_to_object('a.b.c', 1) -> {'a': {'b': {'c': 1}}}

    Args:
        key (str): The dot-separated key to nest the value under
        value (any): The value to nest in the dictionary
    Returns:
        dict: The nested dictionary
    """

    keys = key.split('.')
    result = {}
    current_dict = result

    for k in keys[:-1]:
        current_dict[k] = {}
        current_dict = current_dict[k]

    current_dict[keys[-1]] = value
    return result

