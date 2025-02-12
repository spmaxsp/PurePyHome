
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

