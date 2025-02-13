from .logger import get_logger

from .data_types.creation_info import EntityCreationInfo, check_entity_creation_info
from .data_types.state_info import EntityStateInfo, EntityHistoryInfo
from .data_types.datatype_correction import check_and_correct_value_type

from .signals.register_entity import _register_entity
from .signals.update_entity import _update_entity
from .signals.remove_entity import _remove_entity
from .db.entity_db import entity_db


logger = get_logger()

def create_entity(new_entity: EntityCreationInfo) -> None:
    """Creates an entity in the database and emits the register_entity signal
        The Function checks the EntityCreationInfo for errors before creating the entity.

    Args:
        new_entity (EntityCreationInfo): The info about the new entity
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
    

def update_entity(sender: str, entity_id: str, value, callstack: list) -> None:
    """Updates an entity value in the database and emits the update_entity signal.
        It uses the callstack to prevent infinite loops.
        It also checks if the entity exists.
        The Function accepts the value in any type and tries to convert it to the correct type if possible/needed.

    Args:
        sender (str): The sender requesting the update
        entity_id (str): The entity id
        value (any): The new value 
        callstack (list): The callstack to prevent infinite loops
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
    
    # correct the value type if needed
    try:
        corr_value = check_and_correct_value_type(value, entity.data_type)
    except ValueError as e:
        logger.error(f'Error: {e}')
        return

    current_value = entity.value
    entity_db.update_entity(entity_id, corr_value)
    
    callstack.append(sender)
    _update_entity.send(None, entity_id=entity_id, value=corr_value, last_value=current_value, callstack=callstack)


def remove_entity(entity_id: str) -> None:
    """Removes an entity from the database and emits the remove_entity signal

    Args:
        entity_id (str): The entity id
    Returns:
        None
    """

    entity_db.remove_entity(entity_id)

    _remove_entity.send(None, entity_id=entity_id)


def get_entity(entity_id: str) -> EntityStateInfo:
    """Gets an entity from the database
        (Wrapper for the entity_db.get_entity function)
    
    Args:
        entity_id (str): The entity id
    Returns:
        entity (EntityStateInfo): The info about the entities current state
    """
    
    return entity_db.get_entity(entity_id)


def get_entity_history(entity_id: str) -> EntityHistoryInfo:
    """Gets the history of an entity from the database
        (Wrapper for the entity_db.get_entity_history function)

    Args:
        entity_id (str): The entity id
    Returns:
        history (EntityHistoryInfo): The info about the entities history
    """

    return entity_db.get_entity_history(entity_id)
