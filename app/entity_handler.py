from app.entity_db import entity_data_base
from app.actions_phraser import ActionsPhraser
import yaml

class EntityHandler:
    def __init__(self):
        self.app = None
        self.entities = {}
        self.push_update_callbacks = {}

    def init_app(self, app):
        self.app = app

    def open_entity_yaml(self, yaml_path):
        self.app.logger.info(f'entity_handler::: Loading entities from {yaml_path}')
        try:
            with open(yaml_path, 'r') as f:
                entities_raw = f.read()
                entities = yaml.safe_load(entities_raw)
                self.entities.update(entities)
        except Exception as e:
            self.app.logger.error(f'entity_handler::: Error reading file: {e}')
            return
        
    def get_all_entities(self):
        return self.entities
    
    def register_push_update_callback(self, module_id, callback):
        self.push_update_callbacks[module_id] = callback
        self.app.logger.info(f'entity_handler::: Registered push update callback for module {module_id}')

    def remove_push_update_callback(self, module_id):
        if module_id in self.push_update_callbacks:
            del self.push_update_callbacks[module_id]
            self.app.logger.info(f'entity_handler::: Removed push update callback for module {module_id}')

    def update_entity(self, entity_id, entity_data, event_source, call_stack):
        if entity_id in call_stack:
            self.app.logger.error(f'entity_handler::: Circular reference detected: {call_stack}')
            return

        # Update entity in database
        self.app.logger.info(f'entity_handler::: Updating entity {entity_id} with value {entity_data}')
        entity_data_base.update_entity(entity_id, entity_data)

        #dbg: print all entities
        tmp = entity_data_base.get_all_entities()
        self.app.logger.debug(f'entity_handler::: List of entities:')
        for entity in tmp:
            self.app.logger.debug(f'entity_handler:::   * Entity: {entity.entity_id} - {entity.value}')

        # run actions and update entities
        if entity_id in self.entities:
            if "actions" in self.entities[entity_id]:
                for action in self.entities[entity_id]["actions"]:
                    if next(iter(action)) == "on_update":
                        actions_phraser = ActionsPhraser()
                        actions_phraser.setup(self.app.logger, entity_data, call_stack)
                        actions_phraser.phrase_action(action["on_update"])
                    elif next(iter(action)) == "on_change":
                        if entity_data != entity_data_base.get_entity(entity_id).last_value:
                            actions_phraser = ActionsPhraser()
                            actions_phraser.setup(self.app.logger, entity_data, call_stack)
                            actions_phraser.phrase_action(action["on_change"])

        # publish data if needed
        #if entity_id in self.entities:
        #    if "data_sink" in self.entities[entity_id]:
        #        self.app.logger.info(f'entity_handler::: Publishing data for entity {entity_id}')
        #        if "mqtt" in self.entities[entity_id]["data_sink"]:
        #            if event_source != "mqtt":
        #                from app.mqtt import mqtt_data_publisher
        #                mqtt_data_publisher.publish_entity(entity_id, entity_data)

        # update ui
        if entity_id in self.entities:
            from app.ui_socketio import dashboard_data_publisher
            dashboard_data_publisher.publish_data(entity_id, entity_data) 

        # push update to modules
        for module_id in self.push_update_callbacks:
            self.app.logger.info(f'entity_handler::: Pushing update to module {module_id}')
            self.push_update_callbacks[module_id](entity_id, entity_data)



entity_handler = EntityHandler()
