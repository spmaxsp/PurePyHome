from purepyhome.core.logger import get_logger

from .sqlalchemy import db
from .models import EntityData, EntityHistoric
from .convert import convert_to_db_str, db_entry_to_dict, db_entries_to_id_list, entry_hisory_to_dict

from datetime import datetime
from contextlib import contextmanager

logger = get_logger()

class EntityDB:
    """EntityDB class
        It handles the temporary storage of entity states

        Attributes:
            db: SQLAlchemy database object used to interact with the database
            app: Flask app object

        Functions:
            init_app: Initialize the app object
            @contextmanager __current_app_context: Context manager for the app object
            create_entity: Create an entity in the database
            update_entity: Update an entity in the database
            get_entity: Get an entity from the database
            get_all_entity_ids: Get all entity ids from the database
            get_all_entity_history: Get all entities from the database
            __add_entity_history: Add an entity to the history table
            __purge_entity_history: Cleans up the history table for an entity
    """

    def __init__(self, db):
        self.db = db
        self.app = None


    def init_app(self, app):
        """Initialize the app object
        """
        self.app = app


    @contextmanager
    def __current_app_context(self):
        
        if self.app is None:
            logger.error("Flask app not initialized")
            return

        try:
            with self.app.app_context():
                yield
        except Exception as e:
            logger.error(f'Error working on db: {e}')
            return


    def create_entity(self, entity_id: str, data_type: str, history_depth: int):
        """Create an entity in the database
        
        Args:
            entity_id (str): The entity id
            data_type (str): The data type of the entity
            history_depth (int): The history depth of the entity
        Returns:
            None
        """

        with self.__current_app_context():
            entity = EntityData(entity_id=entity_id, data_type=data_type, history_depth=history_depth)
            self.db.session.add(entity)
            self.db.session.commit()
            
        logger.info(f'Created db entity {entity_id}')


    def update_entity(self, entity_id: str, new_value: any):
        """Update an entity in the database
        
        Args:
            entity_id (str): The entity id
            value (any): The new value of the entity
        Returns:
            None
        """

        with self.__current_app_context():
            entity = EntityData.query.filter_by(entity_id=entity_id).first()
            if entity:
                entity_data_type = entity.data_type
                new_value = convert_to_db_str(new_value, entity_data_type)
                old_value = entity.value
                old_timestamp = entity.timestamp
                history_depth = entity.history_depth

                entity.value = new_value
                entity.timestamp = datetime.now()
            else:
                logger.error(f'Entity {entity_id} not found')

            self.db.session.commit()

        self.__add_entity_history(entity_id, old_value, old_timestamp)
        self.__purge_entity_history(entity_id, history_depth)
        
        logger.info(f'Updated db entity {entity_id} with value {new_value}')


    def get_entity(self, entity_id):
        """Get an entity from the database
            
        Args:
            entity_id (str): The entity id
        Returns:
            Dict: dict of the entity containing the entity id, value, data type and timestamp
        """

        with self.__current_app_context():
            entity = EntityData.query.filter_by(entity_id=entity_id).first()
            if entity:
                return db_entry_to_dict(entity)
            else:
                logger.error(f'Entity {entity_id} not found')
                return None


    def get_all_entity_ids(self):
        """Get all entity ids from the database

        Args:
            None
        Returns:
            List: list of all entity ids
        """

        with self.__current_app_context():
            entities = EntityData.query.all()
            return db_entries_to_id_list(entities)


    def get_all_entity_history(self, entity_id: str):
        """Get all entities from the database

        Args:
            None
        Returns:
            Dict: dict of all entities
        """

        with self.__current_app_context():
            entry_info = EntityData.query.filter_by(entity_id=entity_id).first()
            entries =  EntityHistoric.query.filter_by(entity_id=entity_id).order_by(EntityHistoric.timestamp.desc()).all()
            
            if entry_info and entries:
                return entry_hisory_to_dict(entries, entry_info)
            else:
                logger.error(f'Entity {entity_id} not found')
                return None


    def __add_entity_history(self, entity_id: str, value: str, timestamp: datetime):
        """Add an entity to the history table
        
        Args:
            entity_id (str): The entity id
            value (str): The value of the entity
            timestamp (datetime): The timestamp of the entity
        Returns:
            None
        """

        with self.__current_app_context():
            entity = EntityHistoric(entity_id=entity_id, value=value, timestamp=timestamp)
            self.db.session.add(entity)
            self.db.session.commit()
            
        logger.info(f'Added db entity history {entity_id}')


    def __purge_entity_history(self, entity_id: str, history_depth: int):
        """Cleans up the history table for an entity so that only the last history_depth entries are kept
        
        Args:
            entity_id (str): The entity id
            history_depth (int): The history depth of the entity
        Returns:
            None
        """

        with self.__current_app_context():
            entity = EntityHistoric.query.filter_by(entity_id=entity_id).order_by(EntityHistoric.timestamp.desc()).all()
            if entity:
                if len(entity) > history_depth:
                    for i in range(history_depth, len(entity)):
                        self.db.session.delete(entity[i])
                        self.db.session.commit()
            else:
                logger.error(f'Entity {entity_id} not found in history table')

    def dbg_printout_db(self):
        """Prints out the database contents
        """

        with self.__current_app_context():
            logger.info(f'=========    Printing out database contents    =========')
            entities = EntityData.query.all()
            logger.info(f'Entities: {len(entities)}')
            for entity in entities:
                logger.info(f'Entity: {entity.entity_id} ({entity.data_type}) = {entity.value} @{entity.timestamp} [depth:{entity.history_depth}]')
            histories = EntityHistoric.query.all()
            logger.info(f'Histories: {len(histories)}')
            for history in histories:
                logger.info(f'History: {history.entity_id} = {history.value} @{history.timestamp}')
            logger.info(f'=========    End of database contents    =========')


entity_db = EntityDB(db)