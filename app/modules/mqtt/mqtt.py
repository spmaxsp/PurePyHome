from flask_mqtt import Mqtt as FlaskMqtt
from app.modules.base_module import BaseModule, ModuleInfo

from .mqtt_data_subscriber import MqttDataSubscriber
from .mqtt_data_publisher import MqttDataPublisher


class Mqtt(BaseModule):
    """ Main class for the MQTT module

    Attributes:
        mqtt (flask_mqtt.Mqtt): The Flask MQTT object
        app (flask.Flask): The Flask app object
        update_entity_callback (callable): Function to update an entity in the entity handler
    Functions:
        init_module: Initialize the module
        on_entity_update: This function is called by the entity handler when an entity is updated
        get_module_info: Get information about the module
        get_initialized: Get the initialized status of the module
    """

    def __init__(self):
        self.app = None
        self.update_entity_callback = None

        self.initialized = False

        self.mqtt = None
        self.mqtt_data_subscriber = None
        self.mqtt_data_publisher = None

    def init_module(self, app, entities, update_entity_callback):
        """ Initialize the MQTT module. The module will initialize the MQTT object and the MQTT data subscriber and publisher

        Args:
            app (flask.Flask): The Flask app object
            entities (dict): Dict of all entities
            update_entity_callback (callable): Function to update an entity in the entity handler
        Returns:
            None
        """

        # Save the app and the update_entity_callback
        self.app = app
        self.update_entity_callback = update_entity_callback

        # Initialize the MQTT object and the MQTT data subscriber and publisher
        self.mqtt = FlaskMqtt(app)
        self.mqtt.init_app(app)
        self.mqtt_data_subscriber = MqttDataSubscriber(self.mqtt)
        self.mqtt_data_subscriber.init_app(app)
        self.mqtt_data_subscriber.build_map(entities)
        self.mqtt_data_publisher = MqttDataPublisher(self.mqtt)
        self.mqtt_data_publisher.init_app(app)
        self.mqtt_data_publisher.build_map(entities)

        # register the MQTT callbacks
        self.mqtt.on_message()(self.handle_mqtt_message)
        self.mqtt.on_connect()(self.handle_connect)

        # set the initialized flag to True
        self.initialized = True

    def on_entity_update(self, entity_id, value):
        """ This function is called by the entity handler when an entity is updated

        Args:
            entity_id (str): The entity ID
            value: The new value of the entity
        Returns:
            None
        """

        if self.initialized:
            self.mqtt_data_publisher.publish_entity(entity_id, value)

    def get_module_info(self):
        """ Get information about the module

        Args:
            None
        Returns:
            ModuleInfo: A named tuple containing information about the module
        """

        return ModuleInfo(
            name='MQTT',
            version='0.1',
            type='main_module',
            author='spmaxsp',
            description='Module for MQTT communication'
        )
    
    def get_initialized(self):
        """ Get the initialized status of the module

        Args:
            None
        Returns:
            bool: True if the module is initialized, False otherwise
        """

        return self.initialized

    def handle_mqtt_message(self, client, userdata, message):
        """ Handler for incomming MQTT messages, calls the handle_mqtt_message function of the mqtt_data_subscriber

        Args:
            client: The client
            userdata: The userdata
            message: The message
        Returns:
            None
        """

        if self.initialized:
            self.mqtt_data_subscriber.handle_mqtt_message(client, userdata, message)

    def handle_connect(self, client, userdata, flags, rc):
        """ Handler for MQTT connection, does nothing at the moment

        Args:
            client: The client
            userdata: The userdata
            flags: The flags
            rc: 
        Returns:
            None
        """

        pass






