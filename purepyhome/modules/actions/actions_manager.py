from purepyhome.core.signals.register_entity import connect_to_register_entity
from purepyhome.core.signals.remove_entity import connect_to_remove_entity
from purepyhome.core.signals.update_entity import connect_to_update_entity
from purepyhome.core.logger import get_module_logger

from .actions_phraser import ActionsPhraser

logger = get_module_logger(__name__)

class Actions:
    """Actions class
        It handles the execution of actions for entities, whenever an entity is updated

        Attributes:
            actions: A dictionary that stores the actions for each entity
        Functions:
            on_register_entity: Signal handler for register_entity signal
            on_remove_entity: Signal handler for remove_entity signal
            on_update_entity: Signal handler for update_entity signal
            __register_action: Registers an action for an entity
            __unregister_action: Unregisters an action for an entity
            __run_actions: Runs the actions for an entity

    """

    def __init__(self):
        self.actions = {}

        connect_to_register_entity(self.on_register_entity)
        connect_to_remove_entity(self.on_remove_entity)
        connect_to_update_entity(self.on_update_entity)

    
    def on_register_entity(self, sender, **kwargs):
        """Signal handler for register_entity signal
            Checks if the entity has actions and calls the __register_action function to register the actions

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
            entity_id = new_entity.entity_id
            actions = new_entity.actions

            for action in actions:
                if next(iter(action)) == "on_update":
                    self.__register_action(entity_id, "on_update", action["on_update"])
                elif next(iter(action)) == "on_change":
                    self.__register_action(entity_id, "on_change", action["on_change"])


    def on_remove_entity(self, sender, **kwargs):
        """Signal handler for remove_entity signal
            Calls the __unregister_action function

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
            self.__unregister_action(entity_id)

    
    def on_update_entity(self, sender, **kwargs): 
        """Signal handler for update_entity signal
            Calls the __run_actions function to run the actions for the entity

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
            self.__run_actions(entity_id, value, last_value, callstack)


    def __register_action(self, entity_id, action_type, action):
        """Registers an action for an entity
        Args:
            entity_id: The entity id
            action_type: The action type: on_update, on_change
            action: The action to be registered
        Returns:
            None
        """

        if entity_id not in self.actions:
            self.actions[entity_id] = []
        self.actions[entity_id].append({"action_type": action_type, "action": action})
        logger.info(f'Registered action {action_type} for entity {entity_id}')

    def __unregister_action(self, entity_id):
        """Unregisters an action for an entity
        Args:
            entity_id: The entity id
        Returns:
            None
        """

        if entity_id in self.actions:
            del self.actions[entity_id]
            logger.info(f'Unregistered actions for entity {entity_id}')


    def __run_actions(self, entity_id, value, last_value, callstack):
        """Runs the actions for an entity
        Args:
            entity_id: The entity id
            value: The value of the entity
        Returns:
            None
        """

        if entity_id in self.actions:
            for action in self.actions[entity_id]:
                if action["action_type"] == "on_update":
                    actions_phraser = ActionsPhraser()
                    actions_phraser.setup(logger, value, callstack)
                    actions_phraser.phrase_action(action["action"])
                elif action["action_type"] == "on_change":
                    if value != last_value:
                        actions_phraser = ActionsPhraser()
                        actions_phraser.setup(logger, value, callstack)
                        actions_phraser.phrase_action(action["action"])

actions_manager = Actions()