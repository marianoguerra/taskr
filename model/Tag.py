from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from Task import *

class Tag(Base):
    """
    This class represents a Tag for Tasks
    """
    __tablename__ = 'tag'

    identifier = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    def __init__(self, name='', identifier=None):
        """
        Constructor.
        """
        self.name = name
        self.identifier = identifier

class TagsByTasks(Base):
    __tablename__ = 'tags_by_tasks'

    id_tag = Column(Integer, ForeignKey('tag.identifier'), primary_key=True)
    id_task = Column(Integer, ForeignKey('task.identifier'), primary_key=True)
