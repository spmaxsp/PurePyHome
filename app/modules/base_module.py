from abc import ABC, abstractmethod
from typing import NamedTuple
import flask

class ModuleInfo(NamedTuple):
    name: str
    version: str
    type: str
    author: str
    description: str

class BaseModule(ABC):
    @abstractmethod
    def init_module(self, app: flask.Flask, entities: dict, update_entity_callback: callable) -> None:
        """ Initialize the module
        Args:
            app (flask.Flask): The Flask app object
            entities (dict): Dict of all entities
            update_entity_callback (callable): Function to update an entity in the entity handler
        Returns:
            None
        """
        pass

    @abstractmethod
    def on_entity_update(self, entity_id: str, value) -> None:
        """ This function is called by the entity handler when an entity is updated
        Args:
            entity_id (str): The entity ID
            value: The new value of the entity
        Returns:
            None
        """
        pass

    @abstractmethod
    def get_module_info(self) -> ModuleInfo:
        """ Get information about the module
        Args:
            None
        Returns:
            ModuleInfo: A named tuple containing information about the module
        """
        pass