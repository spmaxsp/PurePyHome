from purepyhome.core.logger import get_logger

from blinker import Namespace

_entity_signals = Namespace()

logger = get_logger()

"""
    Signal to remove registered entities all over the application
"""

_remove_entity = _entity_signals.signal('remove_entity', """
                                            Signal emitted when an entity is removed""")


def connect_to_remove_entity(signal_handler):
    """Connects a signal handler to the remove_entity signal
    
    Args:
        signal_handler: The signal handler
    Returns:
        None
    """
    _remove_entity.connect(signal_handler)