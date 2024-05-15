from purepyhome.core.mqtt import mqtt
from purepyhome.core.signals.register_entity import connect_to_register_entity
from purepyhome.core.signals.remove_entity import connect_to_remove_entity
from purepyhome.core.signals.update_entity import connect_to_update_entity
from purepyhome.core.utils import nest_data_to_object
from purepyhome.core.logger import get_module_logger

import json

logger = get_module_logger(__name__)

class MqttPublisher:
    """MqttPublisher class
        It handles the publishing of data to mqtt topics, whenever an entity is updated
        It listens to the signals: 
            register_entity, remove_entity, update_entity
        ... once a new entity is registered, all updates to the entity will be published to the mqtt topic that the entity is mapped to

        Attributes:
            map: A dictionary that maps entities to topics and keys

        Functions:
            on_register_entity: Signal handler for register_entity signal
            on_remove_entity: Signal handler for remove_entity signal
            on_update_entity: Signal handler for update_entity signal
            __register_entity: Registers an entity to a mqtt topic
            __unregister_entity: Unregisters an entity from a mqtt topic
            __publish_entity: Publishes data to a mqtt topic

    """

    def __init__(self):
        self.map = {}

        connect_to_register_entity(self.on_register_entity)
        connect_to_remove_entity(self.on_remove_entity)
        connect_to_update_entity(self.on_update_entity)


    def on_register_entity(self, sender, **kwargs):
        """Signal handler for register_entity signal
            Checks if the entity has a mqtt data sink and calls the __register_entity function

        Args:
            sender: The sender of the signal
            kwargs: The signal parameters
        Returns:
            None
        """

        try:
            entity_id = kwargs.get('entity_id')
            entity_info = kwargs.get('entity')
        except Exception as e:
            logger.error(f'Error getting required parameters: {e}')
            return
        else:
            if "data_sink" in entity_info:
                if "mqtt" in entity_info["data_sink"]:
                    if "topic" in entity_info["data_sink"]["mqtt"]:
                        topic = entity_info["data_sink"]["mqtt"]["topic"]
                        if "key" in entity_info["data_sink"]["mqtt"]:
                            key = entity_info["data_sink"]["mqtt"]["key"]
                        else:
                            key = ""
                        self.__register_entity(entity_id, topic, key)


    def on_remove_entity(self, sender, **kwargs):
        """Signal handler for remove_entity signal
            Calls the __unregister_entity function

        Args:
            sender: The sender of the signal
            kwargs: The signal parameters
        Returns:
            None
        """

        try:
            entity_id = kwargs.get('entity_id')
        except Exception as e:
            logger.error(f'Error getting required parameters: {e}')
            return
        else:
            self.__unregister_entity(entity_id)


    def on_update_entity(self, sender, **kwargs):
        """Signal handler for update_entity signal
            Calls the __publish_entity function

        Args:
            sender: The sender of the signal
            kwargs: The signal parameters
        Returns:
            None
        """

        try:
            entity_id = kwargs.get('entity_id')
            value = kwargs.get('value')
            last_value = kwargs.get('last_value')
            callstack = kwargs.get('callstack')
        except Exception as e:
            logger.error(f'Error getting required parameters: {e}')
            return
        else:
            self.__publish_entity(entity_id, value)


    def __register_entity(self, entity, topic, key):
        """Registers an entity to a mqtt topic

        Args:
            entity: The entity to be registered
            topic: The mqtt topic
            key: The key to be used to nest the data in the json object
        Returns:
            None
        """

        if entity not in self.map:
            self.map[entity] = []
        self.map[entity].append({"topic": topic, "key": key})
        logger.info(f'mqtt_data_publisher::: Mapped entity {entity} to topic {topic} with key {key}')


    def __unregister_entity(self, entity):
        """Unregisters an entity from a mqtt topic

        Args:
            entity: The entity to be unregistered
        Returns:
            None
        """

        if entity in self.map:
            self.map.pop(entity)
            logger.info(f'mqtt_data_publisher::: Unmapped entity {entity}')


    def __publish_entity(self, entity, data):
        """Publishes data to a mqtt topic

        Args:
            entity: The entity to be published
            data: The data to be published
        Returns:
            None
        """

        if entity in self.map:
            for entry in self.map[entity]:
                topic = entry["topic"]
                key = entry["key"]
                data = nest_data_to_object(key, data)
                logger.info(f'mqtt_data_publisher::: Publishing data {data} to topic {topic}')
                mqtt.publish(topic, json.dumps(data))


mqtt_publisher = MqttPublisher()