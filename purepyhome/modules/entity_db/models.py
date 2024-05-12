from purepyhome.core.db.sqlalchemy import db

from sqlalchemy.sql import func

"""This file provides the EntityData model for the SQLAlchemy DB
    Its used in the entity_db module
"""

class EntityData(db.Model):
    """EntityData model for SQLAlchemy DB
    """

    __tablename__ = 'entity_data'
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(80), nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())
    last_value = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        """EntityData model representation
        """
        return f'<Entity {self.entity_id} = {self.value}>'
