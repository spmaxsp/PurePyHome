from flask_socketio import SocketIO
from app.entity_handler import entity_handler
from app.entity_db import db, entity_data_base
import yaml


class DashboardDataSubscriber:
    def __init__(self, socketio):
        self.map = {}
        self.socketio = socketio
        self.app = None

    def init_app(self, app):
        self.app = app

    def reset_mapping(self):
        self.map = {}

    def register_ui_element(self, entity_id, ui_element):

        if entity_id not in entity_handler.get_all_entities():
            self.app.logger.error(f'entity_handler::: Entity {entity_id} does not exist')
            return
        
        if ui_element not in self.map:
            self.map[ui_element] = []
        self.map[ui_element].append(entity_id)
        self.app.logger.info(f'ui_socketio::: Registered entity {entity_id} for ui element {ui_element}')

    def build_map_from_layout_yaml(self, yaml_path):
        self.app.logger.info(f'ui_socketio::: Loading layout from {yaml_path}')
        try:
            with open(yaml_path, 'r') as f:
                layout_raw = f.read()
                layout = yaml.safe_load(layout_raw)
        except Exception as e:
            self.app.logger.error(f'ui_socketio::: Error reading file: {e}')
            return
        
        for col in layout:
            if next(iter(col)) == "col":
                for card in col["col"]:
                    if next(iter(card)) == "card":
                        if "content" in card["card"]:
                            for content in card["card"]["content"]:
                                if next(iter(content)) == "gauge":
                                    if "data" in content["gauge"] and "id" in content["gauge"]:
                                        self.register_ui_element(content["gauge"]["data"], content["gauge"]["id"])
                                elif next(iter(content)) == "slider":
                                    if "data" in content["slider"] and "id" in content["slider"]:
                                        self.register_ui_element(content["slider"]["data"], content["slider"]["id"])
                    elif next(iter(card)) == "mini-card":
                        if "data" in card["mini-card"] and "id" in card["mini-card"]:
                            self.register_ui_element(card["mini-card"]["data"], card["mini-card"]["id"])

        print (self.map)

    def handle_dashboard_data(self, data):
        self.app.logger.info(f'ui_socketio::: Received data {data}')
        if next(iter(data)) in self.map:
            for entity_id in self.map[next(iter(data))]:
                entity_handler.update_entity(entity_id, data[next(iter(data))], "ui", [])
                self.app.logger.info(f'ui_socketio::: Updated entity {entity_id} with value {data[next(iter(data))]}')

class DashboardDataPublisher:
    def __init__(self, socketio):
        self.map = {}
        self.socketio = socketio
        self.app = None

    def init_app(self, app):
        self.app = app

    def reset_mapping(self):
        self.map = {}

    def register_ui_element(self, entity_id, ui_element):
        #TODO: Add error handling:
        #   - Check if ui_element exists
        if entity_id not in entity_handler.get_all_entities():
            self.app.logger.error(f'entity_handler::: Entity {entity_id} does not exist')
            return

        if entity_id not in self.map:
            self.map[entity_id] = []
        self.map[entity_id].append(ui_element)
        self.app.logger.info(f'ui_socketio::: Registered ui element {ui_element} for entity {entity_id}')
        
    def publish_data(self, entity_id, data):
        if entity_id in self.map:
            for ui_element in self.map[entity_id]:
                self.socketio.emit('dashboard_data', data={ui_element: data})
                self.app.logger.info(f'ui_socketio::: Published data {data} to ui element {ui_element}')

    def publish_all_data(self):
        self.app.logger.info(f'ui_socketio::: Publishing current state to all ui elements')
        for entity_id in self.map:
            entity = entity_data_base.get_entity(entity_id)
            self.publish_data(entity_id, entity.value)

    def build_map_from_layout_yaml(self, yaml_path):
        self.app.logger.info(f'ui_socketio::: Loading layout from {yaml_path}')
        try:
            with open(yaml_path, 'r') as f:
                layout_raw = f.read()
                layout = yaml.safe_load(layout_raw)
        except Exception as e:
            self.app.logger.error(f'ui_socketio::: Error reading file: {e}')
            return
        
        for col in layout:
            if next(iter(col)) == "col":
                for card in col["col"]:
                    if next(iter(card)) == "card":
                        if "content" in card["card"]:
                            for content in card["card"]["content"]:
                                if next(iter(content)) == "gauge":
                                    if "data" in content["gauge"] and "id" in content["gauge"]:
                                        self.register_ui_element(content["gauge"]["data"], content["gauge"]["id"])
                                elif next(iter(content)) == "slider":
                                    if "data" in content["slider"] and "id" in content["slider"]:
                                        self.register_ui_element(content["slider"]["data"], content["slider"]["id"])
                    elif next(iter(card)) == "mini-card":
                        if "data" in card["mini-card"] and "id" in card["mini-card"]:
                            self.register_ui_element(card["mini-card"]["data"], card["mini-card"]["id"])

        print (self.map)
                        
                            



socketio = SocketIO(logger=False, engineio_logger=False)
dashboard_data_publisher = DashboardDataPublisher(socketio)
dashboard_data_subscriber = DashboardDataSubscriber(socketio)

@socketio.on('dashboard_data')
def handle_dashboard_data(data):#
    dashboard_data_subscriber.handle_dashboard_data(data)
    
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    dashboard_data_publisher.publish_all_data()
    