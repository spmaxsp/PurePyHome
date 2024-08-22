from purepyhome.core.socketio import socketio
from purepyhome.core.core import update_entity
from purepyhome.core.logger import get_module_logger

import json

logger = get_module_logger(__name__)

class SocketIoReceiver:
    """SocketIoReceiver class
        It handles the receiving of all updates to the entities from the socket io clients
        Likewise to the Emitter there is no need to register entities

        Attributes:
            None
        Functions:
            on_update_entity: Event handler for update_entity event
            __update_entity: Updates the entity in the database
    """

    def __init__(self):
        socketio.on_event('update_entity_to_serv', self.on_update_entity)


    def on_update_entity(self, data):
        """Event handler for update_entity event

        Args:
            data: The event data
        Returns:
            None
        """

        try:
            entity_id = data.get('entity_id')
            value = data.get('value')
        except Exception as e:
            logger.error(f'Error getting required parameters: {e}')
            return
        else:
            self.__update_entity(entity_id, value)


    def __update_entity(self, entity_id, value):
        """Updates the entity in the database

        Args:
            entity_id: The entity id
            value: The new value
        Returns:
            None
        """

        logger.debug(f'Updating entity: {entity_id} - {value}')
        update_entity("__name__", entity_id, value, [])

ui_io_receiver = SocketIoReceiver()