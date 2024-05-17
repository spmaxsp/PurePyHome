from purepyhome.core.socketio import socketio
from purepyhome.core.signals.update_entity import connect_to_update_entity
from purepyhome.core.logger import get_module_logger

import json

logger = get_module_logger(__name__)

class SocketIoEmitter:
    """SocketIoEmitter class
        It handles the emitting all updates to the entities to the socket io clients
        It listens to the signals: 
            update_entity
        There is no need to register entities, as all updates are emitted to all clients

        Attributes:
            None
        Functions:
            on_update_entity: Signal handler for update_entity signal
            __emit_entity: Emits the entity update to all clients
    """

    def __init__(self):
        connect_to_update_entity(self.on_update_entity)


    def on_update_entity(self, sender, **kwargs):
        """Signal handler for update_entity signal

        Args:
            sender: The sender of the signal
            kwargs: The signal parameters
        Returns:
            None
        """

        try:
            entity_id = kwargs.get('entity_id')
            value = kwargs.get('value')
        except Exception as e:
            logger.error(f'Error getting required parameters: {e}')
            return
        else:
            self.__emit_entity(entity_id, value)


    def __emit_entity(self, entity_id, value):
        """Emits the entity update to all clients

        Args:
            entity_id: The entity id
            entity_info: The entity information
        Returns:
            None
        """

        logger.debug(f'Emitting entity update: {entity_id} - {value}')
        socketio.emit('entity_update_from_serv', {'entity_id': entity_id, 'value': value})

ui_io_emitter = SocketIoEmitter()