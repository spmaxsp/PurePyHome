from purepyhome.core.logger import get_logger

from blinker import Namespace

_entity_signals = Namespace()

logger = get_logger()


"""
    Signal used to retrieve entities and their data all over the application
"""

_get_entity = _entity_signals.signal('get_entity', """
                                            Signal emitted when an entity is retrieved""")


def get_entity_over_signal(entity_id):
    """Retrieves an entity using the get_entity signal
        always returns the first response - there should only be one if not something is wrong

    Args:
        entity_id: The entity id
    Returns:
        EntityData: The entity data object
    """
    
    response = _get_entity.send(None, entity_id=entity_id)

    if len(response) != 1:
        logger.error(f'Error: Multiple or no instances returned for signal get_entity: {response}')
        return None

    reciever, entity = response[0]
    return entity


def connect_to_get_entity(signal_handler):
    """Connects a signal handler to the get_entity signal (also prevents multiple connections)

    Args:
        signal_handler: The signal handler
    Returns:
        None
    """

    if len(_get_entity.receivers) == 0:
        _get_entity.connect(signal_handler)
    else:
        logger.error(f'Error: Multiple connections to get_entity signal: {_get_entity.receivers}')
