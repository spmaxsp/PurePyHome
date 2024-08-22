from purepyhome.core.db.sqlalchemy import db

from sqlalchemy.sql import func

"""This file provides the EntityData and EntityHistoric model for the SQLAlchemy DB
    The EntityData model and table is used to store the current state and metadata of an entity
    The EntityHistoric model and table is used to store the historic values of an entity
"""

class EntityData(db.Model):
    """EntityData model for SQLAlchemy DB
    """

    __tablename__ = 'entity_data'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.String(80), unique=True, nullable=False)
    data_type = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(80), nullable=True)
    last_value = db.Column(db.String(80), nullable=True)
    history_depth = db.Column(db.Integer, nullable=False)

    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())


    def __repr__(self):
        """EntityData model representation
        """
        return f'<Entity {self.entity_id} = {self.value} @{self.timestamp}>'


class EntityHistoric(db.Model):
    """EntityHistoric model for SQLAlchemy DB
    """

    __tablename__ = 'entity_historic'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(80), nullable=True)

    timestamp = db.Column(db.DateTime(timezone=True))

    def __repr__(self):
        """EntityHistoric model representation
        """
        return f'<Historic of {self.entity_id} = {self.value} @{self.timestamp}>'