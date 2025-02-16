from purepyhome.core.mqtt import mqtt
from purepyhome.core.value_converters.value_conversers import run_value_converter
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
            new_entity = kwargs.get('new_entity')
            if new_entity is None:
                raise ValueError(f'Canot find parameter: new_entity')

        except Exception as e:
            logger.error(f'Error getting required parameters: {e}')
            return
        else:
            if new_entity.data_sink.sink_type == "mqtt":
                entity_id = new_entity.entity_id
                sink_info = new_entity.data_sink.sink_info


                if "topic" in sink_info:
                    topic = sink_info["topic"]

                    if "key" in sink_info:
                        key = sink_info["key"]
                    else:
                        key = ""

                    converter_name = new_entity.data_sink.converter_name
                    converter_info = new_entity.data_sink.converter_info

                    self.__register_entity(entity_id, topic, key, converter_name, converter_info)


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


    def __register_entity(self, entity, topic, key, converter_name, converter_info):
        """Registers an entity to a mqtt topic

        Args:
            entity: The entity to be registered
            topic: The mqtt topic
            key: The key to be used to nest the data in the json object
            converter_name: The name of the data converter
            converter_info: Additional info for the data converter
        Returns:
            None
        """

        if entity not in self.map:
            self.map[entity] = []
        self.map[entity].append({"topic": topic, "key": key, "converter_name": converter_name, "converter_info": converter_info})
        logger.info(f'Mapped entity {entity} to topic {topic} with key {key} (uses converter {converter_name})')


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
        """Publishes data to a mqtt topic for an entity (after converting the data)

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
                converter_name = entry["converter_name"]
                converter_info = entry["converter_info"]

                data_conv = run_value_converter(data, converter_name, converter_info, True)

                if key != "":
                    data_obj = nest_data_to_object(key, data_conv)
                    data = json.dumps(data_obj)
                else:
                    data = str(data_conv)
                    
                logger.info(f'mqtt_data_publisher::: Publishing data {data} to topic {topic}')
                mqtt.publish(topic, data)


mqtt_publisher = MqttPublisher()