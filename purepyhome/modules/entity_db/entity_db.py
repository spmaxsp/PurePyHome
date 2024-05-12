from purepyhome.core.db.sqlalchemy import db
from purepyhome.core.signals import register_entity, update_entity, remove_entity, get_entity
from purepyhome.core.utils import detect_color_and_convert
from purepyhome.core.logger import get_module_logger

from .models import EntityData

from datetime import datetime

logger = get_module_logger(__name__)

class EntityDB:
    """EntityDB class
        It handles the temporary storage of entity states
        It listens to the signals: 
            register_entity, update_entity, remove_entity, get_entity 
        ... and updates the database accordingly

        Attributes:
            db: SQLAlchemy database object used to interact with the database
            app: Flask app object

        Functions:
            init_app: Initialize the app object
            on_register_entity: Signal handler for register_entity signal
            on_update_entity: Signal handler for update_entity signal
            on_get_entity: Signal handler for get_entity signal
            __create_entity: Create an entity in the database
            __update_entity: Update an entity in the database
            __get_entity: Get an entity from the database
            get_all_entities: Get all entities from the database
    """

    def __init__(self, db):
        self.db = db
        self.app = None

        register_entity.connect(self.on_register_entity)
        update_entity.connect(self.on_update_entity)
        get_entity.connect(self.on_get_entity)


    def init_app(self, app):
        """Initialize the app object
        """
        self.app = app


    def on_register_entity(self, sender, **kwargs):
        """Signal handler for register_entity signal

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
            self.__create_entity(entity_id)


    def on_update_entity(self, sender, **kwargs):
        """Signal handler for update_entity signal
        
        Args:
            sender: The sender of the signal
            kwargs: The signal parameters
        Returns:
            None
        """

        try:
            entity_id = kwargs.get('entity_id')
            value = kwargs.get('value')
        except Exception as e:
            logger.error(f'Error getting required parameters: {e}')
            return
        else:
            self.__update_entity(entity_id, value)


    def on_get_entity(self, sender, **kwargs):
        """Signal handler for get_entity signal

        Args:
            sender: The sender of the signal
            kwargs: The signal parameters
        Returns:
            EntityData: The entity data object
        """

        try:
            entity_id = kwargs.get('entity_id')
        except Exception as e:
            logger.error(f'Error getting required parameters: {e}') 
            return
        else:
            return self.__get_entity(entity_id)


    def __create_entity(self, entity_id):
        """Create an entity in the database
        
        Args:
            entity_id (str): The entity id
            entity_type (str): The entity type
        Returns:
            None
        """

        if self.app is None:
            logger.error("Flask app not initialized")
            return
        
        try:
            entity = EntityData(entity_id=entity_id, type='string')
            with self.app.app_context():
                db.session.add(entity)
                db.session.commit()
        except Exception as e:
            logger.error(f'Error creating entity: {e}')
            return
            
        logger.info(f'Created db entity {entity_id}')


    def __update_entity(self, entity_id, value):
        """Update an entity in the database
            For now, the value is always a string. This will be changed in the future
        
        Args:
            entity_id (str): The entity id
            value: The new value of the entity
        Returns:
            None
        """

        if self.app is None:
            logger.error("Flask app not initialized")
            return

        try:
            with self.app.app_context():
                entity = EntityData.query.filter_by(entity_id=entity_id).first()

                if entity:
                    entity.last_value = entity.value
                    entity.value = str(value)
                    entity.timestamp = datetime.now()

                # if entity:
                #     if entity.type == 'int':
                #         value = str(value)
                #     elif entity.type == 'bool':
                #         value = 'True' if value else 'False'
                #     elif entity.type == 'int_list_10':
                #         value = ','.join(str(x) for x in entity.value.split(',')[:9] + [str(value)])
                #     elif entity.type == 'string':
                #         value = str(value)
                #     elif entity.type == 'rgb':
                #         value = detect_color_and_convert(value) or entity.value
                #     entity.last_value = entity.value
                #     entity.value = value
                #     entity.timestamp = datetime.now()

                db.session.commit()
        except Exception as e:
            logger.error(f'Error updating entity: {e}')
            return
        
        logger.info(f'Updated db entity {entity_id} with value {value}')


    def __get_entity(self, entity_id):
        """Get an entity from the database
            
        Args:
            entity_id (str): The entity id
        Returns:
            EntityData: The entity data object
        """

        if self.app is None:
            logger.error("Flask app not initialized")
            return None

        try:
            with self.app.app_context():
                entity = EntityData.query.filter_by(entity_id=entity_id).first()
                if entity:
                    return entity
                else:
                    return None
        except Exception as e:
            logger.error(f'Error getting entity: {e}')
            return None


    def get_all_entities(self):
        """Get all entities from the database

        Args:
            None
        Returns:
            Dict: dict of all entities
        """

        if self.app is None:
            logger.error("Flask app not initialized")
            return None
        
        try:
            with self.app.app_context():
                return EntityData.query.all()
        except Exception as e:
            logger.error(f'Error getting all entities: {e}')
            return None


entity_db = EntityDB(db)