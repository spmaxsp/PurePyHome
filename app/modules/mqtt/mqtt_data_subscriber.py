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