from __future__ import absolute_import

import logging

from celery.beat import Scheduler, ScheduleEntry
from celery.schedules import maybe_schedule
from celery.utils.log import get_logger

logger = get_logger(__name__)


class StoreEntry(ScheduleEntry):

    def __init__(self, periodic_task):
        self.periodic_task = periodic_task
        self.task = periodic_task.get_task()
        self.name = periodic_task.name
        self.args = periodic_task.args
        self.kwargs = periodic_task.kwargs
        self.options = periodic_task.options
        self.last_run_at = periodic_task.last_run_at

    def is_due(self):
        if self.periodic_task.is_active:
            return self.schedule.is_due(self.last_run_at)
        return False, 5.0  # 5 second delay for re-enable.

    def __next__(self):
        return self.__class__(self.periodic_task)

    next = __next__  # for 2to3


class StoreScheduler(Scheduler):
    Entry = StoreEntry

    def __init__(self, *args, **kwargs):
        self._schedule = None
        self._has_made_initial_read = False
        self.app = current_app._get_current_object()
        self.PeriodicTask = kwargs.get('PeriodicTask')
        self.TaskSchedule = kwargs.get('TaskSchedule')
        self._latest_change = self.TaskSchedule.get_latest_change_to_schedule()
        super(StoreScheduler, self).__init__(*args, **kwargs)

    def schedule_changed(self):
        latest_change = self.PeriodicTask.get_latest_change_to_schedule()
        try:
            if latest_change and latest_change > (self._latest_change
                                                if self._latest_change
                                                else latest_change):
                return True
        finally:
            self._latest_change = latest_change
        return False

    def setup_schedule(self):
        self.install_default_entries(self.schedule)
        self.update_from_dict(self.app.conf.CELERYBEAT_SCHEDULE)

    def all_as_schedule(self):
        logger.debug('{0}: Fetching database schedule'.format(
            self.__class__.__name__, 
        ))
        entries = {}
        for periodic_task in self.PeriodicTask.get_all_with_active_schedules():
            try:
                entries[task.name] = self.Entry(periodic_task)
            except ValueError:
                pass
        return entries

    def sync(self):
        logger.info('Writing Task Schedule Store Entries')
        self._schedule = self.all_as_schedule()

    @property
    def schedule(self):
        update = False
        if self._has_made_initial_read:
            logger.info('{0}: initial read'.format(
                self.__class__.__name__, 
            ))
            update = True
        elif self.schedule_changed():
            logger.info('{0}: Schedule changed'.format(
                self.__class__.__name__, 
            ))
            update = True

        if update:
            self.sync()
            if logger.isEnabledFor(logging.DEBUG):
                _msg_schedule = '\n'.join(
                    repr(entry) for entry in self._schedule.values()
                )
                logger.debug('Current Schedule:\n{0}'.format(_msg_schedule))
        return self._schedule
