from __future__ import absolute_import


class PeriodicTaskMixin(object):

    @property
    def name(self):
        raise NotImplementedError

    def get_schedules(self):
        raise NotImplementedError

    @classmethod
    def get_all_with_active_schedules(cls):
        raise NotImplementedError

    def get_task(self):
        '''
        :returns: actual celery task function
        '''
        raise NotImplementedError

    @property
    def is_active(self):
        return True

    @property
    def args(self):
        return (,)

    @property
    def kwargs(self):
        return {}

    @property
    def last_run_at(self):
        raise NotImplementedError

    @property
    def total_run_count(self):
        raise NotImplementedError

    @property
    def options(self):
        '''
        return {
            'queue': self.queue,
            'exchange': self.exchange,
            'routing_key': self.routing_key,
            'expires': self.expires,
        }
        
        '''
        raise NotImplementedError

    @classmethod
    def get_latest_change_to_schedule(cls):
        '''
        Returns the most recent change that was made to the schedule
        entry in your backend.

        :rtype: datetime.datetime
        '''
        raise NotImplementedError



class TaskScheduleMixin(object):


    @property
    def task(self):
        '''
        Returns an instance of PeriodicTaskMixin
        '''
        raise NotImplementedError
