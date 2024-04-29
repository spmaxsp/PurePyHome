from flask_mqtt import Mqtt
import yaml
from app.entity_handler import entity_handler

from app.helper import get_nested_value, nest_data_to_object

import json

# sorts out what mqtt toppics are subscribed and what entities are mapped to them
class MqttDataSubscriber:
    def __init__(self, mqtt):
        self.map = {}
        self.mqtt = mqtt
        self.app = None

    def init_app(self, app):
        self.app = app

    def reset_mapping(self):
        self.map = {}

    def register_entity(self, topic, entity, key):
        #TODO: Add error handling:
        #   - Check if topic exists
        #   - Check if entity exists
        if topic not in self.map:
            self.map[topic] = {}
        if entity not in self.map[topic]:
            self.map[topic][key] = []
        self.map[topic][key].append(entity)

    def handle_mqtt_message(self, client, userdata, message):
        data = message.payload.decode()
        try:
            data = json.loads(data)
        except:
            self.app.logger.info(f'mqtt_data_subscriber::: Could not parse message payload to json')
            return
        topic = message.topic
        self.app.logger.info(f'mqtt_data_subscriber::: Received message on topic {topic}')
        for key in self.map[topic]:
            value = get_nested_value(data, key)
            if value is not None:
                for entity in self.map[topic][key]:
                    self.app.logger.info(f'mqtt_data_subscriber::: Updating entity {entity} with value {value}')
                    entity_handler.update_entity(entity, value, "mqtt", [])
            
    def update_subscriptions(self):
        self.app.logger.info(f'mqtt_data_subscriber::: Update subscriptions')
        self.mqtt.unsubscribe_all()
        for topic in self.map:
            self.mqtt.subscribe(topic)
            self.app.logger.info(f'mqtt_data_subscriber::: Subscribed to topic {topic}')

    def build_map_from_yaml(self, yaml_path):
        try:
            with open(yaml_path, 'r') as f:
                entities_raw = f.read()
                entities = yaml.safe_load(entities_raw)
                self.build_map(entities)
        except Exception as e:
            self.app.logger.error(f'mqtt_data_subscriber::: Error reading file: {e}')
            return
        
    def build_map(self, entities):
        for entity in entities:
            if "data_source" in entities[entity]:
                if "mqtt" in entities[entity]["data_source"]:
                    if "topic" in entities[entity]["data_source"]["mqtt"]:
                        topic = entities[entity]["data_source"]["mqtt"]["topic"]
                        if "key" in entities[entity]["data_source"]["mqtt"]:
                            key = entities[entity]["data_source"]["mqtt"]["key"]
                        else:
                            key = ""
                        self.register_entity(topic, entity, key)
                        self.app.logger.info(f'mqtt_data_subscriber::: Mapped topic {topic} with key {key} to entity {entity}')
        self.update_subscriptions()


class MqttDataPublisher:
    def __init__(self, mqtt):
        self.map = {}
        self.mqtt = mqtt
        self.app = None

    def init_app(self, app):
        self.app = app

    def reset_mapping(self):
        self.map = {}

    def register_entity(self, entity, topic, key):
        #TODO: Add error handling:
        #   - Check if topic exists
        #   - Check if entity exists
        if entity not in self.map:
            self.map[entity] = []
        self.map[entity].append({"topic": topic, "key": key})

    def publish_entity(self, entity, data):
        for entry in self.map[entity]:
            topic = entry["topic"]
            key = entry["key"]
            data = nest_data_to_object(key, data)
            self.app.logger.info(f'mqtt_data_publisher::: Publishing data {data} to topic {topic}')
            self.mqtt.publish(topic, json.dumps(data))

    def build_map(self, entities):
        for entity in entities:
            if "data_sink" in entities[entity]:
                if "mqtt" in entities[entity]["data_sink"]:
                    if "topic" in entities[entity]["data_sink"]["mqtt"]:
                        topic = entities[entity]["data_sink"]["mqtt"]["topic"]
                        if "key" in entities[entity]["data_sink"]["mqtt"]:
                            key = entities[entity]["data_sink"]["mqtt"]["key"]
                        else:
                            key = ""
                        self.register_entity(entity, topic, key)
                        self.app.logger.info(f'mqtt_data_publisher::: Mapped entity {entity} to topic {topic} with key {key}')            



mqtt = Mqtt()
mqtt_data_subscriber = MqttDataSubscriber(mqtt)
mqtt_data_publisher = MqttDataPublisher(mqtt)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    mqtt_data_subscriber.handle_mqtt_message(client, userdata, message)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    pass





