'''REST API for Taskr'''
import tubes
import intertubes

import model
from model import Task, Tag

handler = tubes.Handler()
handler.register_static_path('/static', 'static/')

PORT = 8080

@handler.get("^/$", accepts=tubes.HTML)
def index(req):
    return tubes.redirect('/static/index.html', code=302)

@handler.post("^/task/$", accepts=tubes.JSON)
def create_task(req, data):
    """create a new Task"""
    task = model.Task.from_dict(data)
    identifier = model.manager.create(task)
    return model.manager.to_dict(task)

@handler.put("^/task/$", accepts=tubes.JSON)
def modify_task(req, data):
    """modify an existing Task"""
    task = model.Task.from_dict(data)
    model.manager.modify(task)
    return model.manager.to_dict(task)

@handler.get("^/task/(\\d+)$")
def get_task(req, identifier):
    """return a Task identified by id if exists"""
    task = model.manager.get(int(identifier))

    if task is None:
        return tubes.Response('task not found', 404)

    return model.manager.to_dict(task)

@handler.delete("^/task/(\\d+)$")
def delete_task(req, identifier):
    """remove a Task identified by id if exists"""
    identifier = int(identifier)

    if identifier is None:
        return

    succeeded = model.manager.delete(identifier)

    if not succeeded:
        return tubes.Response('task not found', 404)

@handler.get("^/tasks/$")
def get_tasks(req,):
    """return the tasks"""
    tasks = model.manager.get_tasks()
    return model.manager.tasks_to_dict(tasks)

@handler.get("^/tags/$")
def get_tags(req,):
    """return the tags"""
    tags = model.manager.get_tags()
    return model.manager.tags_to_dict(tags)

@handler.get("^/task-by/tag/(.+)$")
def task_by_tag(req, tag):
    """return all the tasks that contain the tag"""
    tasks = model.manager.get_by_tag(tag)
    return model.manager.tasks_to_dict(tasks)

@handler.get("^/task-by/priority/(\\d)$")
def task_by_priority(req, priority):
    """return all the tasks where priority is set to 'priority'"""
    tasks = model.manager.get_by_priority(int(priority))
    return model.manager.tasks_to_dict(tasks)

@handler.get("^/task-by/date/after/(\\d+)$")
def task_after(req, timestamp):
    """return all the tasks where end_date starts after timestamp"""
    tasks = model.manager.get_from_timestamp(int(timestamp))
    return model.manager.tasks_to_dict(tasks)

@handler.get("^/task-by/date/between/(\\d+)/(\\d+)$")
def task_between(req, from_t, to_t):
    """return all the tasks where"""
    tasks = model.manager.get_between(int(from_t), int(to_t))
    return model.manager.tasks_to_dict(tasks)

@handler.get("^/task-by/expired$")
def tasks_expired(req,):
    """return all the tasks where"""
    tasks = model.manager.get_expired()
    return model.manager.tasks_to_dict(tasks)

@handler.get('^/requests.js/?$', produces=tubes.JS)
def requests(req):
    '''return the requests.js file to interact with this API'''
    return tubes.Response(REQUESTS)

@handler.get('^/model.js/?$', produces=tubes.JS)
def get_model(req):
    '''return the model.js file to interact with this API'''
    return MODEL

@handler.get('^/test.html/?$', produces=tubes.HTML)
def test(req):
    '''return a dummy html to play with the API'''
    return TEST_PAGE

REQUESTS = intertubes.generate_requests(handler)
MODEL = intertubes.generate_model([Tag, Task], "Taskr", False)
TEST_PAGE = intertubes.generate_html_example(handler,
        ('/static/js/json2.js', '/model.js'))

if __name__ == '__main__':
    tubes.run(handler, port=PORT, use_reloader=True, use_debugger=True)
