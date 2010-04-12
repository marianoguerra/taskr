import time

from Task import Tag
from Task import Task
from Task import Session

from sqlalchemy import and_

class TaskManager(object):
    """
    This class represents a manager for the Task class
    """

    def __init__(self):
        """
        Constructor.
        """
        self.session = Session()

    def create(self, task):
        """
        create and store a task

        task -- a Task object
        """
        new_tags, task.tags = self._sync_tags(task.tags)

        for tag in task.tags:
            if task not in tag.tasks:
                tag.tasks.append(task)

        self.session.add(task)

        for tag in new_tags:
            tag.tasks.append(task)
            task.tags.append(tag)
            self.session.add(tag)

        self.session.commit()
        return task

    def modify(self, new_task):
        """
        modify the fields of a task

        task -- a Task object
        """
        task = self.get(new_task.identifier)

        if task is None:
            return None

        task.name = new_task.name
        task.description = new_task.description
        task.priority = new_task.priority
        task.end = new_task.end
        task.finished = new_task.finished

        new_tags, task.tags = self._sync_tags(new_task.tags)

        for tag in task.tags:
            if task not in tag.tasks:
                tag.tasks.append(task)


        self.session.update(task)

        for tag in new_tags:
            tag.tasks.append(task)
            task.tags.append(tag)
            self.session.add(tag)

        self.session.commit()
        return task

    def _sync_tags(self, tags):
        """
        try to retrieve the tags that already are in the database
        """
        old_tags = []
        new_tags = []

        for tag in tags:
            sync_tag = self.session.query(Tag).get(tag.name)
            if sync_tag is None:
                new_tags.append(tag)
            else:
                old_tags.append(sync_tag)

        return new_tags, old_tags

    def get(self, identifier):
        """
        return a task identified by id

        identifier -- the id
        """
        return self.session.query(Task).get(identifier)

    def to_dict(self, task):
        """
        return a JSON string representing a task object

        task -- the Task object to serialize
        """
        return task.vars()

    def delete(self, identifier):
        """
        delete the task identifier by id

        identifier -- the task id
        """
        self.session.delete(self.get(identifier))

    def get_by_tag(self, name):
        """
        return all the tasks taged with a tag
        """
        tag = self.session.query(Tag).filter(Tag.name==name).all()
        if tag is not None:
            return tag[0].tasks

        return ()

    def tasks_to_dict(self, tasks):
        """
        return a JSON string representing a list of tasks

        tasks -- a list of tasks
        """
        return [task.vars() for task in tasks]

    def get_by_priority(self, priority):
        """
        return all the tasks with priority set to priority value

        priority -- the value of the priority
        """
        return self.session.query(Task).filter(Task.priority==priority)

    def get_from_timestamp(self, timestamp):
        """
        return all the tasks that expire after timestamp

        timestamp -- the timestamp
        """
        return self.session.query(Task).filter(Task.end>timestamp)

    def get_between(self, from_t, to_t):
        """
        return the Tasks that expire between from_t and to_t

        from_t -- the timestamp from
        to_t -- the timestamp to
        """
        return self.session.query(Task).filter(and_(Task.end>from_t, Task.end < to_t))

    def get_expired(self):
        """
        return the task that are not finished and end is less that current time
        """
        now = time.time()
        return self.session.query(Task).filter(and_(Task.end<now, Task.finished==False))

    def get_tasks(self):
        """
        return all the tags
        """
        return self.session.query(Task).all()

    def get_tags(self):
        """
        return all the tags
        """
        return self.session.query(Tag).all()

    def tags_to_dict(self, tags):
        """
        return a JSON string representing a list of Tag objects

        tags -- a list og Tag objects
        """
        return [tag.vars() for tag in tags]

manager = TaskManager()
