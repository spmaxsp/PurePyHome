from purepyhome.core.logger import get_logger

from purepyhome.core.signals.get_entity import get_entity_over_signal

from blinker import Namespace

_entity_signals = Namespace()

logger = get_logger()


"""
    Signal used to update entities all over the application in a standardized way
"""

_update_entity = _entity_signals.signal('update_entity', """
                                            Signal emitted when an entity is updated""")


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
    _update_entity.send(None, entity_id=entity_id, value=value, last_value=current_value, callstack=callstack)


def connect_to_update_entity(signal_handler):
    """Connects a signal handler to the update_entity signal

    Args:
        signal_handler: The signal handler
    Returns:
        None
    """

    _update_entity.connect(signal_handler)