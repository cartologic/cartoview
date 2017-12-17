from .models import Task
from threading import Thread, Timer
import datetime
from django.core.exceptions import ObjectDoesNotExist
import logging
from sys import stdout
from importlib import import_module

import json
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s  { %(name)s %(pathname)s:%(lineno)d} \
                            %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


class TaskAlreadyRunningException(BaseException):
    message = "Task Already Running"


class TaskTypeException(BaseException):
    message = "Wrong Task Type"


class CartoviewTask(object):
    def __init__(self, task, task_arg=[],
                 task_kwargs={}, type=Task.A_PERIODIC, every=0):
        if type not in [Task.A_PERIODIC, Task.PERIODIC]:
            raise TaskTypeException()
        self.id = None
        self.task = task
        self.task_arg = task_arg
        self.type = type
        self.every = every
        self.task_kwargs = task_kwargs

    def create_task(self):
        task = Task.objects.create(
            type=self.type, every=self.every,
            started_at=datetime.datetime.now(),
            status=Task.IN_PROGRESS)
        self.id = task.id

    def _run_save(self):
        result = self.task(*self.task_arg, **self.task_kwargs)
        try:
            cartoview_task = Task.objects.get(id=self.id)
            if cartoview_task.type == Task.A_PERIODIC:
                cartoview_task.finished_at = datetime.datetime.now()
                cartoview_task.status = Task.FINISHED
            if result:
                cartoview_task.result = json.dumps(result)
            cartoview_task.save()
            if cartoview_task.type == Task.PERIODIC:
                time_in_seconds = cartoview_task.every * 60 * 60
                Timer(time_in_seconds, self._run_save).start()
        except ObjectDoesNotExist as ex:
            logger.error(ex.message)

    def _execute(self, target, task_args=[], task_kwargs={}):
        thread = Thread(target=target, args=tuple(
            task_args), kwargs=task_kwargs)
        thread.daemon = True
        thread.start()

    def execute_async(self):
        if not self.id:
            self.create_task()
            self._execute(self._run_save)
            return self.id
        else:
            raise TaskAlreadyRunningException()

    def execute_forget(self):
        self._execute(self.task, self.task_args, self.task_kwargs)


def import_from_module(string_package_module):
    package, module = string_package_module.rsplit('.', 1)
    package = import_module(package)
    imported = getattr(package, module)
    return imported
