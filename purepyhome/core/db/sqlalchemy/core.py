
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model

class PurePyHomeSQLAlchemy(SQLAlchemy):
    """ Custom SQLAlchemy class for PurePyHome

    This class is a custom Wrapper around the SQLAlchemy class. 
    It can be used to add custom functionality to the SQLAlchemy class if needed.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

db = PurePyHomeSQLAlchemy()