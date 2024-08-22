from purepyhome.core.logger import get_logger

from blinker import Namespace

_entity_signals = Namespace()

logger = get_logger()


"""
    Signal used to update entities all over the application in a standardized way
"""

_update_entity = _entity_signals.signal('update_entity', """
                                            Signal emitted when an entity is updated""")


def connect_to_update_entity(signal_handler):
    """Connects a signal handler to the update_entity signal

    Args:
        signal_handler: The signal handler
    Returns:
        None
    """

    _update_entity.connect(signal_handler)