from purepyhome.core.logger import get_logger

from blinker import Namespace

_entity_signals = Namespace()

logger = get_logger()


"""
    Signal to register entities all over the application
"""

_register_entity = _entity_signals.signal('register_entity', """
                                            Signal emitted when a new entity is registered""")


def connect_to_register_entity(signal_handler):
    """Connects a signal handler to the register_entity signal

    Args:
        signal_handler: The signal handler
    Returns:
        None
    """
    _register_entity.connect(signal_handler)









