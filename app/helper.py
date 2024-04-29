import colorsys
import re

def hsl_to_rgb(hsl):
    hsl_values = hsl.strip('hsl()').split(',')
    h, s, l = int(hsl_values[0]), int(hsl_values[1]) / 100, int(hsl_values[2]) / 100
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l, s)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return f"rgb({r},{g},{b})"

def rgb_to_rgb(rgb):
    return rgb

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def detect_color_and_convert(color):
    if color.startswith("hsl"):
        return hsl_to_rgb(color)
    elif color.startswith("rgb"):
        return rgb_to_rgb(color)
    elif re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        return hex_to_rgb(color)
    else:
        return False
    
def get_nested_value(obj, key):
    keys = key.split('.')
    try:
        value = obj
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return None
    
def nest_data_to_object(key, value):
    keys = key.split('.')
    result = {}
    current_dict = result

    for k in keys[:-1]:
        current_dict[k] = {}
        current_dict = current_dict[k]

    current_dict[keys[-1]] = value
    return result
    
