import yaml
from datetime import datetime

from sqlalchemy.sql import func

from flask_sqlalchemy import SQLAlchemy

from app.helper import detect_color_and_convert

db = SQLAlchemy()
class EntityData(db.Model):
    __tablename__ = 'entity_data'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(80), nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    last_value = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f'<Entity {self.entity_id} = {self.value}>'
    

class EntityDataBase:
    def __init__(self, db=None):
        self.app = None
        self.db = db

    def init_app(self, app):
        self.app = app

    def init_db(self):
        with self.app.app_context():
            self.db.drop_all()
            self.db.create_all()

    def create_entity(self, entity_id, entity_type):
        valid_types = ['int', 'bool', 'int_list_10', 'string', 'rgb']

        if entity_type not in valid_types:
            raise ValueError(f'Invalid entity type: {entity_type}')
        
        with self.app.app_context():
            entity = EntityData(entity_id=entity_id, type=entity_type)

        with self.app.app_context():
            self.db.session.add(entity)
            self.db.session.commit()
            
        self.app.logger.info(f'entity_data_base::: Created entity {entity_id} with type {entity_type}')

    def update_entity(self, entity_id, value):
        with self.app.app_context():
            entity = EntityData.query.filter_by(entity_id=entity_id).first()
            if entity:
                if entity.type == 'int':
                    value = str(value)
                elif entity.type == 'bool':
                    value = 'True' if value else 'False'
                elif entity.type == 'int_list_10':
                    value = ','.join(str(x) for x in entity.value.split(',')[:9] + [str(value)])
                elif entity.type == 'string':
                    value = str(value)
                elif entity.type == 'rgb':
                    value = detect_color_and_convert(value) or entity.value
                entity.last_value = entity.value
                entity.value = value
                entity.timestamp = datetime.now()

                self.db.session.commit()
                return True
            else:
                return False

    def get_entity(self, entity_id):
        with self.app.app_context():
            entity = EntityData.query.filter_by(entity_id=entity_id).first()
        if entity:
            return entity
        else:
            return None

    def get_all_entities(self):
        with self.app.app_context():
            return EntityData.query.all()

    def build_db_from_yaml(self, yaml_path):
        try:
            with open(yaml_path, 'r') as f:
                entities_raw = f.read()
                entities = yaml.safe_load(entities_raw)
                self.build_db(entities)
        except Exception as e:
            error_message = f'Error reading file: {e}'
            print(error_message)
            return

    def build_db(self, entities):
        for entity in entities:
            self.create_entity(entity, "string")

entity_data_base = EntityDataBase(db)

