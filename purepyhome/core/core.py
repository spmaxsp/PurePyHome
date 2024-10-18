from .logger import get_logger

from .data_types.creation_info import EntityCreationInfo, check_entity_creation_info

from .signals.register_entity import _register_entity
from .signals.update_entity import _update_entity
from .signals.remove_entity import _remove_entity
from .db.entity_db import entity_db


logger = get_logger()

def create_entity(new_entity: EntityCreationInfo):
    """Creates an entity in the database and emits the register_entity signal

    Args:
        new_entity: The new entity creation info
    Returns:
        None
    """

    try:
        check_entity_creation_info(new_entity)
    except ValueError as e:
        logger.error(f'Error: {e}')
        return

    entity_db.create_entity(new_entity.entity_id, new_entity.data_type, new_entity.history_depth)

    _register_entity.send(None, new_entity=new_entity)
    

def update_entity(sender: str, entity_id: str, value, callstack: list):
    """Updates an entity value in the database and emits the update_entity signal
        uses the callstack to prevent infinite loops

    Args:
        sender: The sender requesting the update
        entity_id: The entity id
        value: The new value
        callstack: The callstack to prevent infinite loops
    Returns:
        None
    """

    # check for circular reference
    if sender in callstack:
        #logger.error(f'Error: Circular reference detected: {callstack}')
        return

    # get the entity from the database
    entity = entity_db.get_entity(entity_id)

    # check if the entity exists
    if entity is None:
        #logger.error(f'Error: Entity {entity_id} not found')
        return

    current_value = entity['value']
    entity_db.update_entity(entity_id, value)
    
    callstack.append(sender)
    _update_entity.send(None, entity_id=entity_id, value=value, last_value=current_value, callstack=callstack)


def remove_entity(entity_id: str):
    """Removes an entity from the database and emits the remove_entity signal

    Args:
        entity_id: The entity id
    Returns:
        None
    """

    entity_db.remove_entity(entity_id)

    _remove_entity.send(None, entity_id=entity_id)


def get_entity(entity_id: str):
    """Gets an entity from the database
    
    Args:
        entity_id (str): The entity id
    Returns:
        entity: The entity value
    """
    
    return entity_db.get_entity(entity_id)


def get_entity_history(entity_id: str):
    """Gets the history of an entity from the database

    Args:
        entity_id (str): The entity id
    Returns:
        history: The entity history
    """

    return entity_db.get_entity_history(entity_id)
