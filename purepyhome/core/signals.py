from purepyhome.core.logger import get_logger

from blinker import Namespace

_entity_signals = Namespace()

logger = get_logger()


register_entity = _entity_signals.signal('register_entity', """
                                            Signal emitted when a new entity is registered""")

update_entity = _entity_signals.signal('update_entity', """
                                            Signal emitted when an entity is updated""")

remove_entity = _entity_signals.signal('remove_entity', """
                                            Signal emitted when an entity is removed""")

get_entity = _entity_signals.signal('get_entity', """
                                            Signal emitted when an entity is retrieved""")


def update_entity_over_signal(sender: str, entity_id: str, value, callstack: list):
    """Updates an entity using the update_entity signal
        uses the callstack to prevent infinite loops
    Args:
        sender: The sender of the signal
        entity_id: The entity id
        value: The new value
        callstack: The callstack to prevent infinite loops
    Returns:
        None
    """

    if sender in callstack:
        logger.error(f'Error: Circular reference detected: {callstack}')
        return
    
    current_value = get_entity_over_signal(entity_id).value
    
    callstack.append(sender)
    update_entity.send(None, entity_id=entity_id, value=value, last_value=current_value, callstack=callstack)


def get_entity_over_signal(entity_id):
    """Retrieves an entity using the get_entity signal
        always returns the first response - there should only be one if not something is wrong
    Args:
        entity_id: The entity id
    Returns:
        EntityData: The entity data object
    """
    
    response = get_entity.send(None, entity_id=entity_id)

    if len(response) != 1:
        logger.error(f'Error: Multiple or no instances returned for signal get_entity: {response}')
        return None

    reciever, entity = response[0]
    return entity
