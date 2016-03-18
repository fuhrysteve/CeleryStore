import datetime as dt

from celery_store.mixins import PeriodicTaskMixin, TaskScheduleMixin


class PeriodicTask(PeriodicTaskMixin):
    
    def __init__(self, *args, **kwargs):
        self.name = 'My Task'

    def get_schedules(self):
        schedule = TaskSchedule()
        schedule.task = self
        return [schedule]

    @classmethod
    def get_latest_change_to_schedule(cls):
        return dt.datetime.now() - dt.timedelta(minutes=5)

class TaskSchedule(TaskScheduleMixin):
    pass
