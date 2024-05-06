
from .mqtt.mqtt import Mqtt

#mqtt_module = Mqtt()  # does work here

class ModuleManager():

    def __init__(self):
        self.mqtt_module = None

    def init_modules(self, app, entity_handler):
        """ Initialize all modules
        Args:
            app (flask.Flask): The Flask app object
            entity_handler (EntityHandler): The entity handler object
        Returns:
            None
        """
        self.mqtt_module = Mqtt()   # does not work
        self.mqtt_module.init_module(app, entity_handler.get_all_entities(), entity_handler.update_entity)

        entity_handler.register_push_update_callback('mqtt', self.mqtt_module.on_entity_update)
        
        #self.modules.append(mqtt_module)