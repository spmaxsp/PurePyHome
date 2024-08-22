from .models import EntityData, EntityHistoric
from purepyhome.core.data_types.creation_info import ENTITY_DATA_TYPES

def convert_to_db_str(value, type) -> str:
    
    if type not in ENTITY_DATA_TYPES:
        raise ValueError(f'Type {type} not in {ENTITY_DATA_TYPES}')
    
    if type == 'string':
        if isinstance(value, str):
            return value
        raise ValueError(f'Value {value} not of type string')
    
    elif type == 'numeric':
        if isinstance(value, (float, int)):
            return str(float(value))
        raise ValueError(f'Value {value} not of type numeric')
    
    elif type == 'bool':
        if isinstance(value, bool):
            return "True" if value == True else "False"
        raise ValueError(f'Value {value} not of type bool')
    
    elif type == 'color':
        if isinstance(value, (tuple)) and len(value) == 3:
            if all(isinstance(i, int) for i in value):
                return f'{value[0]},{value[1]},{value[2]}'
        raise ValueError(f'Value {value} not of type color (tuple of 3 ints)')
    
    elif type == 'time':
        raise NotImplementedError('Time type not implemented')
    
    else:
        raise ValueError(f'Type {type} not implemented')



def convert_from_db_str(value, type) -> any:
    
    if type not in ENTITY_DATA_TYPES:
        raise ValueError(f'Type {type} not in {ENTITY_DATA_TYPES}')
    
    if type == 'string':
        return value
    
    elif type == 'numeric':
        return float(value)
    
    elif type == 'bool':
        return True if value == "True" else False
    
    elif type == 'color':
        return tuple(int(x) for x in value.split(','))
    
    elif type == 'time':
        raise NotImplementedError('Time type not implemented')
    
    else:
        raise ValueError(f'Type {type} not implemented')



def db_entry_to_dict(entry: EntityData) -> dict:
    res = {}
    res['entity_id']  = entry.entity_id 
    res['value']      = convert_from_db_str(entry.value, entry.data_type)
    res['last_value'] = convert_from_db_str(entry.last_value, entry.data_type)
    res['data_type']  = entry.data_type
    res['timestamp']  = entry.timestamp
    
    return res

def db_entries_to_id_list(entries: list) -> list:
    res = []
    for entry in list:
        res.append(entry.entity_id)

    return res


def entry_hisory_to_dict(entries: list, entry_info: EntityData) -> dict:
    res = {}
    res['entity_id']  = entry_info.entity_id 
    res['values']      = []
    res['data_type']  = entry_info.data_type

    for entry in entries:
        res['values'].append({'value': convert_from_db_str(entry.value, entry_info.data_type),
                              'timestamp': entry.timestamp
                              })
        
    return res