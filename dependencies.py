
tasks_db = {}

def _set_next_id():
    next_id = 1
    while True:
        yield next_id
        next_id += 1

_counter = _set_next_id()

def get_next_id():
    return next(_counter)


# создать функцию get_task_by_id