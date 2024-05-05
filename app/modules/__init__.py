
from .mqtt import Mqtt

class ModuleManager():

    def __init__(self):
        self.modules = []

    def init_modules(self, app, entity_handler):
        """ Initialize all modules
        Args:
            app (flask.Flask): The Flask app object
            entity_handler (EntityHandler): The entity handler object
        Returns:
            None
        """
        mqtt = Mqtt()
        mqtt.init_module(app, entity_handler.get_all_entities(), entity_handler.update_entity)

        entity_handler.register_push_update_callback('mqtt', mqtt.on_entity_update)
        
        self.modules.append(mqtt)