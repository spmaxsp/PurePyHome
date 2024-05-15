from purepyhome.core.logger import get_logger

from blinker import Namespace

_entity_signals = Namespace()

logger = get_logger()


"""
    Signal to register entities all over the application
"""

_register_entity = _entity_signals.signal('register_entity', """
                                            Signal emitted when a new entity is registered""")


def register_entity_over_signal(entity_id: str, entity_info: dict):
    """Registers an entity using the register_entity signal

    Args:
        entity_id: The entity id
        entity_info: The entity information
    Returns:
        None
    """
    _register_entity.send(None, entity_id=entity_id, entity=entity_info)


def connect_to_register_entity(signal_handler):
    """Connects a signal handler to the register_entity signal

    Args:
        signal_handler: The signal handler
    Returns:
        None
    """
    _register_entity.connect(signal_handler)









