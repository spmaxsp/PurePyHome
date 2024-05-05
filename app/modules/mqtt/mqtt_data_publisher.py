from app.helper import get_nested_value, nest_data_to_object
import json

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
