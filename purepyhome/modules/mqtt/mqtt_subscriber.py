from purepyhome.core.mqtt import mqtt
from purepyhome.core.data_types.creation_info import EntityCreationInfo
from purepyhome.core.signals.register_entity import connect_to_register_entity
from purepyhome.core.signals.remove_entity import connect_to_remove_entity
from purepyhome.core.core import update_entity
from purepyhome.core.utils import get_nested_value
from purepyhome.core.logger import get_module_logger

import json

logger = get_module_logger(__name__)

class MqttSubscriber:
    """MqttSubscriber class
        It handles the subscription to mqtt topics and updates the entities accordingly
        It listens to the signals: 
            register_entity, remove_entity 
        ... once a new entity is registered, it subscribes to the mqtt topic
            when a mqtt message is received, it updates the entities that are mapped to the topic via the update_entity signal

        Attributes:
            map: A dictionary that maps topics and keys to entities

        Functions:
            on_register_entity: Signal handler for register_entity signal
            on_remove_entity: Signal handler for remove_entity signal
            on_mqtt_message: Handler for incomming MQTT messages
            __handle_mqtt_message: Handles incomming MQTT messages
            __register_entity: Registers an entity to a topic
            __unregister_entity: Unregisters an entity from a topic
    """

    def __init__(self):
        self.map = {}

        connect_to_register_entity(self.on_register_entity)
        connect_to_remove_entity(self.on_remove_entity)

        mqtt.on_message()(self.on_mqtt_message)


    def on_register_entity(self, sender, **kwargs):
        """Signal handler for register_entity signal
            Checks if the entity has a mqtt data source and calls the __register_entity function

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

                    if "topic" in entity_info["data_source"]["mqtt"]:
                        topic = entity_info["data_source"]["mqtt"]["topic"]
                        if "key" in entity_info["data_source"]["mqtt"]:
                            key = entity_info["data_source"]["mqtt"]["key"]
                        else:
                            key = ""
                        self.__register_entity(topic, key, entity_id)


    def on_remove_entity(self, sender, **kwargs):
        """Signal handler for remove_entity signal
            Checks if the entity has a mqtt data source and calls the __unregister_entity function

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
            if "data_source" in entity_info:
                if "mqtt" in entity_info["data_source"]:
                    if "topic" in entity_info["data_source"]["mqtt"]:
                        topic = entity_info["data_source"]["mqtt"]["topic"]
                        if "key" in entity_info["data_source"]["mqtt"]:
                            key = entity_info["data_source"]["mqtt"]["key"]
                        else:
                            key = ""
                        self.__unregister_entity(entity_id)


    def on_mqtt_message(self, client, userdata, message):
        """Handler for incomming MQTT messages
            this function reads the message payload and calls the __handle_mqtt_message function

        Args:
            client: The client
            userdata: The userdata
            message: The message
        Returns:
            None
        """

        try:
            data = message.payload.decode()
            data = json.loads(data)
            topic = message.topic
        except:
            logger.error(f'Could not parse message payload to json')
            return
        else:
            logger.info(f'Received message on topic {topic} with data {data}')
            self.__handle_mqtt_message(topic, data)


    def __handle_mqtt_message(self, topic, data):
        """Handles incomming MQTT messages
            this function calls all update_entity signals for the entities that are mapped to the topic

        Args:
            topic: The topic
            data: The message data
        Returns:
            None
        """

        for key in self.map[topic]:
            value = get_nested_value(data, key)
            if value is not None:
                for entity in self.map[topic][key]:
                    logger.info(f'Updating entity {entity} with value {value}')
                    update_entity(__name__, entity_id=entity, value=value, callstack=[])


    def __register_entity(self, topic, key, entity_id):
        """Registers an entity to a topic
            this function registers the entity to the topic and key in the map and subscribes to the topic

        Args:
            topic: The topic
            key: The key
            entity_id: The entity_id
        Returns:
            None
        """

        if topic not in self.map:   # if the topic is not in the map, add it
            self.map[topic] = {}
        if key not in self.map[topic]:    # if the key is not in the map, add it
            self.map[topic][key] = []
        self.map[topic][key].append(entity_id)  # add the entity to the map

        logger.info(f'Subscribing to topic {topic}')
        mqtt.subscribe(topic)


    def __unregister_entity(self, entity_id):
        """Unregisters an entity from a topic
            this function unregisters the entity from the topic in the map and unsubscribes from the topic if no entity is left

        Args:
            entity_id: The entity_id
        Returns:
            None
        """

        # search for the entity in the map and remove it
        for topic in self.map:
            for key in self.map[topic]:
                if entity_id in self.map[topic][key]:
                    self.map[topic][key].remove(entity_id)

                    if len(self.map[topic][key]) == 0:  # if no entity is left, remove the key
                        del self.map[topic][key]
                        if len(self.map[topic]) == 0:   # if no key is left, remove the topic and unsubscribe
                            del self.map[topic]
                            mqtt.unsubscribe(topic)
                            logger.info(f'Unsubscribed from topic {topic}') 


mqtt_subscriber = MqttSubscriber()
