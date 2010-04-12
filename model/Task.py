from sqlalchemy import create_engine, MetaData, Column, String, Integer, \
    Boolean, Table, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///task.db', echo=True)
meta = MetaData(engine)
Session = sessionmaker(bind=engine)

class Tag(Base):
    """
    This class represents a Tag for Tasks
    """
    __tablename__ = 'tag'

    name = Column(String(64), primary_key=True)

    def __init__(self, name='', tasks=None):
        """
        Constructor.
        """
        self.name = name

        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks

    def vars(self, full=True):
        """return a dict represetation of the object"""
        tasks = None

        if full:
            tasks = [task.vars(False) for task in self.tasks]

        return {"name": self.name, "tasks": tasks}

    @classmethod
    def from_dict(cls, dct, recursive=True):
        """
        return an instance of the class from a dict object
        if recursive is set to True create the tasks contained inside
        """
        tag = cls()
        tag.name = dct['name']
        tag.tasks = []

        if not recursive:
            return tag

        for task in dct.get('tasks', ()):
            tag.tasks.append(Task.from_dict(task, False))

        return tag

class Task(Base):
    """a class that represents a task on a todo list"""
    __tablename__ = 'task'

    identifier = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(String(256))
    end = Column(Integer)
    priority = Column(Integer)
    finished = Column(Boolean)

    def __init__(self, name='', description='', end=0, priority=3,
            finished=False, identifier=None, tags=None):
        """constructor"""
        self.name = name
        self.description = description
        self.priority = priority
        self.end = end
        self.finished = finished
        self.identifier = identifier
        if tags is None:
            self.tags = []
        else:
            self.tags = tags

    def vars(self, full=True):
        """return a dict representation of the vars"""
        tags = None
        if full:
            tags = [tag.vars(False) for tag in self.tags]

        return {"name": self.name, "description": self.description,
                "priority": self.priority, "end": self.end,
                "finished": self.finished, "identifier": self.identifier,
                "tags": tags}

    @classmethod
    def from_dict(cls, dct, recursive=True):
        """
        return an instance of the class from a dict object
        if recursive is set to True create the tags contained inside
        """
        task = cls()
        task.name = dct['name']
        task.identifier = dct.get('identifier', None)
        task.description = dct.get('description', '')
        task.priority = dct.get('priority', 3)
        task.end = dct['end']
        task.finished = dct.get('finished', False)
        task.tags = []

        if not recursive:
            return task

        for tag in dct.get('tags', ()):
            task.tags.append(Tag.from_dict(tag, False))

        return task

TagsByTasks = Table('tags_by_tasks', meta,
    Column('id_tag', Integer, ForeignKey(Tag.name)),
    Column('id_task', Integer, ForeignKey(Task.identifier)))

Task.tags = relation(Tag, secondary=TagsByTasks, backref='Task')
Tag.tasks = relation(Task, secondary=TagsByTasks, backref='Tag')

meta.create_all(engine)
Base.metadata.create_all(engine)
