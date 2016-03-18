import datetime as dt

from celery_store.mixins import PeriodicTaskMixin, TaskScheduleMixin

from celery import current_app as app
from celery.schedules import crontab


@app.task(name='sum-of-two-numbers')
def add(x, y):
    return x + y


class PeriodicTask(PeriodicTaskMixin):
    
    @property
    def name(self):
        return 'My Task'

    def get_schedules(self):
        schedule = TaskSchedule()
        schedule.task = self
        return [schedule]

    def get_task(self):
        return add

    @classmethod
    def get_all_with_active_schedules(cls):
        return [TaskSchedule(), TaskSchedule()]

    @classmethod
    def get_latest_change_to_schedule(cls):
        return dt.datetime.now() - dt.timedelta(minutes=5)

    @property
    def last_run_at(self):
        return dt.datetime.now() - dt.timedelta(seconds=(60*4) + 50)


class TaskSchedule(TaskScheduleMixin):

    @property
    def schedule(self):
        return crontab('*')

    @property
    def task(self):
        task = PeriodicTask()
        task.schedule = self
        return task
