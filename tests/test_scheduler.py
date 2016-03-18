from unittest import TestCase
import datetime as dt

from celery.schedules import crontab
from celery import Celery

from celery_store.mixins import PeriodicTaskMixin, TaskScheduleMixin
from celery_store.scheduler import StoreEntry, StoreScheduler


def UnitApp(name=None, set_as_current=False,
            broker='memory://', backend='cache+memory://', **kwargs):
    app = Celery(name or 'celery.tests',
                 set_as_current=set_as_current,
                 broker=broker, backend=backend,
                 **kwargs)
    return app

celery = UnitApp()
celery.conf['CELERYSTORE_PERIODIC_TASK'] = 'tests.test_scheduler.MockPeriodicTask'
celery.conf['CELERYSTORE_TASK_SCHEDULE'] = 'tests.test_scheduler.MockTaskSchedule'

class MockPeriodicTask(PeriodicTaskMixin):

    def __init__(self, *args, **kwargs):
        self._last_run_at = (dt.datetime.now() -
                             dt.timedelta(seconds=(60*4) + 50))
    
    @property
    def name(self):
        return 'My Task'

    def get_schedules(self):
        schedule = MockTaskSchedule()
        schedule.task = self
        return [schedule]

    def get_task(self):
        return add

    @classmethod
    def get_all_with_active_schedules(cls):
        return [MockTaskSchedule(), MockTaskSchedule()]

    @classmethod
    def get_latest_change_to_schedule(cls):
        return dt.datetime.utcnow() - dt.timedelta(minutes=5)

    @property
    def last_run_at(self):
        return self._last_run_at


class MockTaskSchedule(TaskScheduleMixin):

    @property
    def schedule(self):
        return crontab('*')

    @property
    def task(self):
        if not hasattr(self, '_task'):
            self._task = MockPeriodicTask()
            self._task.schedule = self
        return self._task


class TestStoreEntry(TestCase):

    def test_store_entry_iterates_indefinitely(self):
        ts = MockTaskSchedule()
        entry = StoreEntry(ts)
        for n in range(0, 10):
            next_entry = next(entry)
            self.assertIsInstance(next_entry, StoreEntry)
            self.assertIsInstance(next_entry.schedule, TaskScheduleMixin)
            
    def test_is_not_due(self):
        ts = MockTaskSchedule()
        ts._task = MockPeriodicTask()
        ts._task._last_run_at = dt.datetime.utcnow() + dt.timedelta(days=1)

        entry = StoreEntry(ts)
        is_due, delay = entry.is_due()
        self.assertFalse(is_due)
        self.assertGreater(delay, (24 * 3600) - 100)

    def test_is_due(self):
        ts = MockTaskSchedule()
        ts._task = MockPeriodicTask()
        ts._task._last_run_at = dt.datetime.utcnow() - dt.timedelta(minutes=5)
        entry = StoreEntry(ts)
        is_due, delay = entry.is_due()
        self.assertTrue(is_due)
        self.assertLess(delay, 60.1)

    def test_inactive_never_due(self):
        ts = MockTaskSchedule()
        class MockPeriodicTask2(MockPeriodicTask):
            @property
            def is_active(self):
                return False
        ts._task = MockPeriodicTask2()
        ts._task._last_run_at = dt.datetime.utcnow() - dt.timedelta(days=1)
        entry = StoreEntry(ts)
        is_due, delay = entry.is_due()
        self.assertFalse(is_due)
        self.assertEqual(delay, 5.0)

class TestStoreScheduler(TestCase):

    def test_schedule_changed(self):
        ss = StoreScheduler(app=celery)
        self.assertTrue(ss.schedule_changed())
        ss._latest_change = dt.datetime.utcnow() - dt.timedelta(days=2)

        self.assertTrue(ss.schedule_changed())
        ss._latest_change = dt.datetime.utcnow()
        self.assertFalse(ss.schedule_changed())
